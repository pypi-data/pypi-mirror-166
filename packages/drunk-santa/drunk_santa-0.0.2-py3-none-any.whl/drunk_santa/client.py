import functools
import logging

import requests
from requests.adapters import HTTPAdapter, Retry

from drunk_santa.beer import Beer
from drunk_santa.config import BACKOFF_FACTOR, BASE_URL, STATUS_FORCELIST, TOTAL_RETRIES

logger = logging.getLogger(__name__)
logging.info(f"Session started: {__name__}")


def cached(function):
    cache = {}

    @functools.wraps(function)
    def wrapper(*args, **kwds):

        kwds_aux = kwds
        kwds_aux = frozenset(kwds_aux.items())
        signature = (function, args, kwds_aux)

        if signature in cache:
            logging.info(f"Found in cache {kwds}")
            result = cache[signature]

        else:
            result = function(*args, **kwds)
            cache[signature] = result

        return result

    return wrapper


class DrunkSanta:
    def __init__(self, base_url=None):
        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = BASE_URL

    def request_with_optional_params(
        self,
        url_add=None,
        return_multiple_beers=None,
        params=None,
    ):
        """Request base_url with named optional params"""

        if url_add is not None:
            url = f"{self.base_url}{url_add}"
        else:
            url = f"{self.base_url}"

        try:
            with requests.Session() as session:
                retries = Retry(
                    total=TOTAL_RETRIES,
                    backoff_factor=BACKOFF_FACTOR,
                    status_forcelist=STATUS_FORCELIST,
                )
                session.mount("https://", HTTPAdapter(max_retries=retries))

                response = session.get(url, params=params)
                response.raise_for_status()

                logging.info(response.status_code)

                if return_multiple_beers is not None:
                    return response.json()
                else:
                    return response.json()[0]

        except requests.exceptions.HTTPError:
            if response.status_code == 400:
                raise SystemExit(self.get_response_error_messaje(response))
            else:
                raise SystemExit(response.json().get("message"))

        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

    def get_response_error_messaje(self, response):
        """Parse error info from request"""
        parram = response.json().get("data")[0].get("param")
        error_parram = response.json().get("data")[0].get("msg")
        error_info = response.json().get("message")
        return f"{error_info}: {parram} - {error_parram}"

    def format_ids(self, beers_ids):
        """"""
        return "|".join(beers_ids)

    @cached
    def get_beers(
        self,
        page_number=1,
        per_page=20,
        abv_gt=None,
        abv_lt=None,
        ibu_gt=None,
        ibu_lt=None,
        ebc_gt=None,
        ebc_lt=None,
        beer_name=None,
        yeast=None,
        brewed_before=None,
        brewed_after=None,
        hops=None,
        malt=None,
        food=None,
        ids=None,
    ):
        """Get beers with specified characteristics"""

        if ids is not None:
            ids = self.format_ids(ids)

        params = {
            "page": page_number,
            "per_page": per_page,
            "abv_gt": abv_gt,
            "abv_lt": abv_lt,
            "ibu_gt": ibu_gt,
            "ibu_lt": ibu_lt,
            "ebc_gt": ebc_gt,
            "ebc_lt": ebc_lt,
            "beer_name": beer_name,
            "yeast": yeast,
            "brewed_before": brewed_before,
            "brewed_after": brewed_after,
            "hops": hops,
            "malt": malt,
            "food": food,
            "ids": ids,
        }

        beers = []

        for beer in self.request_with_optional_params(
            params=params, return_multiple_beers=True
        ):
            beers.append(Beer.from_json(beer))
            logging.info(f"Extracted beer id: {Beer.from_json(beer).id}")

        return beers

    @cached
    def get_all_beers(self):
        """Get all the beers"""
        page = 1
        response = self.request_with_optional_params(
            params={"page": page}, return_multiple_beers=True
        )
        while response:
            for beer in response:
                final_beer = Beer.from_json(beer)
                logging.info(f"Extracted beer id: {final_beer.id}")
                yield final_beer

            page += 1
            response = self.request_with_optional_params(
                params={"page": page}, return_multiple_beers=True
            )

    @cached
    def get_beer_by_id(self, beers_id):
        """Get the beers by id"""
        final_beer = Beer.from_json(
            self.request_with_optional_params(url_add=f"/{beers_id}")
        )
        logging.info(f"Extracted beer id: {final_beer.id}")

        return final_beer

    @cached
    def get_random_beer(self):
        """Get a random beer"""
        final_beer = Beer.from_json(
            self.request_with_optional_params(url_add="/random")
        )
        logging.info(f"Extracted beer id: {final_beer.id}")

        return final_beer

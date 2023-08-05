# Standard library imports
import copy
from json import load
import os

# Local imports
from .error import Error

# TODO Instead of loading stale .json files get real-time reference info using this
# https://developer.ebay.com/devzone/xml/docs/reference/ebay/GeteBayDetails.html (this link is stale)


class Reference:
    """ Caches of reference information sourced from eBay's developer website. """

    _cache = {}

    @staticmethod
    def get_application_scopes() -> dict:
        """ Get eBay **Client Credential/Code** Grant Type Scopes
         that might be permitted when minting **Application** tokens.

         Dictionary keys are the scopes, and data are descriptions.

        Source https://developer.ebay.com/my/keys, Sandbox column, click OAuth Scopes, second section

        :return application_scopes (dict)
        """
        return Reference._get('application_scopes')

    @staticmethod
    def get_country_codes() -> dict:
        """ Get eBay country code information.

        A partial list of ISO 3166 standard two-letter codes that represent countries around the world.

        Source https://developer.ebay.com/devzone/xml/docs/reference/ebay/types/countrycodetype.html.

        :return country_codes (dict)
        """
        return Reference._get('country_codes')

    @staticmethod
    def get_currency_codes() -> dict:
        """ Get eBay country code information.

        A partial list of standard 3-digit ISO 4217 currency codes for currency used in countries around the world.

        Source https://developer.ebay.com/devzone/xml/docs/Reference/eBay/types/CurrencyCodeType.html.

        :return currency_codes (dict)
        """
        return Reference._get('currency_codes')

    # TODO if nobody complains then permanently delete otherwise fix code_generate.py
    @staticmethod
    def get_item_fields_modified() -> dict:
        """ Get eBay item "response" field information.

        The root container is ebay_item.

        Details of a specific item can include description, price, category, all item aspects, condition,
        return policies, seller feedback and score, shipping options, shipping costs, estimated delivery,
        and other information the buyer needs to make a purchasing decision.

        This has been modified in an opinionated way to aid with SQL database storage.

        Source https://developer.ebay.com/api-docs/buy/browse/resources/item/methods/getItem#h2-output.

        :return item_fields_modified (dict)
        """
        # return Reference._get('item_fields_modified')
        reason = 'Deprecated; if you need this, make an issue https://github.com/matecsaj/ebay_rest/issues.'
        raise Error(number=95001, reason=reason)

    # TODO if nobody complains then permanently delete otherwise fix code_generate.py
    @staticmethod
    def get_item_enums_modified() -> dict:
        """ Get eBay enumeration type definitions and SOME of their values.

        Beware that many values are missing; expect to encounter new ones.

        This has been modified in an opinionated way to aid with SQL database storage.

        Source https://developer.ebay.com/api-docs/buy/browse/enums.

        :return enums_modified (dict)
        """
        # return Reference._get('item_enums_modified')
        reason = 'Deprecated; if you need this, make an issue https://github.com/matecsaj/ebay_rest/issues.'
        raise Error(number=95002, reason=reason)

    @staticmethod
    def get_global_id_values() -> dict:
        """ Get eBay global id information.

        The Global ID is a unique identifier for combinations of site, language, and territory.
        Global ID values are returned in globalId and are used as input for the X-EBAY-SOA-GLOBAL-ID header.
        The global ID you use must correspond to an eBay site with a valid site ID.
        See https://developer.ebay.com/Devzone/merchandising/docs/Concepts/SiteIDToGlobalID.html
        eBay Site ID to Global ID Mapping for a list of global IDs you can use with the API calls.

        Source https://developer.ebay.com/Devzone/merchandising/docs/CallRef/Enums/GlobalIdList.html.

        :return global_id_values (dict)
        """
        return Reference._get('global_id_values')

    @staticmethod
    def get_marketplace_id_values() -> dict:
        """ Get eBay marketplace id information.

        The following table lists the set of supported Marketplace IDs, their associated countries,
        the URLs to the marketplaces, and the locales supported by each marketplace

        Source https://developer.ebay.com/api-docs/static/rest-request-components.html#marketpl.

        :return marketplace_id_values (dict)
        """
        return Reference._get('marketplace_id_values')

    @staticmethod
    def get_user_scopes() -> dict:
        """ Get eBay **Authorization Code** Grant Type Scopes
        that might be permitted when minting **User Access** tokens.

        Dictionary keys are the scopes, and data are descriptions.

        Source https://developer.ebay.com/my/keys, Sandbox column, click OAuth Scopes, first section

        :return user_scopes (dict)
        """
        return Reference._get('user_scopes')

    @staticmethod
    def _get(name) -> dict:
        """
        Get information from the json files.

        :param name (str, required)
        :return information (dict)
        """
        if name not in Reference._cache:
            # get the path to this python file, which is also where the data file directory is
            path, _fn = os.path.split(os.path.realpath(__file__))
            # to the path join the data file name and extension
            path_name = os.path.join(path, 'references', name + '.json')
            with open(path_name) as file_handle:
                Reference._cache[name] = load(file_handle)
        return copy.deepcopy(Reference._cache[name])

# firebase-dynamic-link-generator

Simple python client to generate [Firebase Dynamic Links](https://firebase.google.com/docs/dynamic-links/). It allows to 
use a custom domain and fields for generate links for android and ios.


### Requirements

* Python >= 3.8
* PIP
* API Key from [Firebase console Settings page](https://console.firebase.google.com/project/_/settings/general/).


### Installation
```bash
pip3 install firebase-dynamic-links-generator
```

### Usage
```python
from firebase_dynamic_link_generator import GenerateFirebaseDynamicLink

SERVICE_FILE	= 'YOUR_SERVICE_ACCOUNT_JSON_FILE_PATH'
DOMAIN 	      = 'example.page.link' ## need to setup in firebase dynamic link
NAME          = "NAME_OF_LINK" ## name of the link

fdl = GenerateFirebaseDynamicLink(DOMAIN, SERVICE_FILE, NAME)
linkinfo_params = {
    "androidInfo": {
        "androidPackageName": 'PACKAGE_NAME',
        "androidFallbackLink": 'FALL_BACK_LINK',
        "androidMinPackageVersionCode": '1'
    },
}

## for short link
short_link = fdl.generate_dynamic_link('http://google.com', linkinfo_params) #https://example.page.link/h77c

## custom short link
suffix_params = {
	"option": "CUSTOM", 		## SHORT or UNGUESSABLE
	"customSuffix": "CT2213" 	## for custom suffix valye

}
short_link = fdl.generate_dynamic_link('http://google.com', linkinfo_params, suffix_params) #https://example.page.link/CT2213
```
* `api_key`: [Key from firebase console](https://console.firebase.google.com/project/_/settings/general/)
* `domain`: Domain uri prefix created in firebase console - Dynamic Link. For example `example.page.link` or your custom domain.
* `linkinfo_params`: Dictionary of optional params. For example:
```python
{
	"domainUriPrefix": string,
    "link": string,
    "androidInfo": {
      "androidPackageName": string,
      "androidFallbackLink": string,
      "androidMinPackageVersionCode": string
    },
    "iosInfo": {
      "iosBundleId": string,
      "iosFallbackLink": string,
      "iosCustomScheme": string,
      "iosIpadFallbackLink": string,
      "iosIpadBundleId": string,
      "iosAppStoreId": string
    },
    "navigationInfo": {
      "enableForcedRedirect": boolean,
    },
    "analyticsInfo": {
      "googlePlayAnalytics": {
        "utmSource": string,
        "utmMedium": string,
        "utmCampaign": string,
        "utmTerm": string,
        "utmContent": string
      },
      "itunesConnectAnalytics": {
        "at": string,
        "ct": string,
        "mt": string,
        "pt": string
      }
    },
    "socialMetaTagInfo": {
      "socialTitle": string,
      "socialDescription": string,
      "socialImageLink": string
    }
}
```

* `suffix_params`: Dictionary of optional params. For example:
```python
{
	"option": "SHORT" or "UNGUESSABLE" or "CUSTOM",
	"customSuffix": string, 
}
```

### Reference
[https://firebase.google.com/docs/dynamic-links/rest](https://firebase.google.com/docs/dynamic-links/rest)  
[https://firebase.google.com/docs/reference/dynamic-links/link-shortener](https://firebase.google.com/docs/reference/dynamic-links/link-shortener)
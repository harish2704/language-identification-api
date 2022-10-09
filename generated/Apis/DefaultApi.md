# DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getApiLanguagePredict**](DefaultApi.md#getApiLanguagePredict) | **GET** /api/language/predict | Get a list of supported languages
[**postApiLanguagePredict**](DefaultApi.md#postApiLanguagePredict) | **POST** /api/language/predict | Detect language of given text


<a name="getApiLanguagePredict"></a>
# **getApiLanguagePredict**
> AvailableLanguagesResponse.3de4f90 getApiLanguagePredict()

Get a list of supported languages

### Parameters
This endpoint does not need any parameter.

### Return type

[**AvailableLanguagesResponse.3de4f90**](../Models/AvailableLanguagesResponse.3de4f90.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

<a name="postApiLanguagePredict"></a>
# **postApiLanguagePredict**
> LanguageDetectionResponse.3de4f90 postApiLanguagePredict(LanguageDetectionRequest.3de4f90)

Detect language of given text

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **LanguageDetectionRequest.3de4f90** | [**LanguageDetectionRequest.3de4f90**](../Models/LanguageDetectionRequest.3de4f90.md)|  | [optional]

### Return type

[**LanguageDetectionResponse.3de4f90**](../Models/LanguageDetectionResponse.3de4f90.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


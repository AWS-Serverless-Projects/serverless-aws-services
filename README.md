# AWS Services per Region

[![](https://img.shields.io/badge/Available-serverless%20app%20repository-blue.svg)](https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:987919146615:applications~aws-services-by-region)


This is a serverless application which provides an API endpoint to get AWS services with available regions.

## Deploy the sample application
This is a serverless application built with SAM. You may deploy this as a normal SAM application.

1. Clone the repository.

2. Install required packages by:
```bash
pip install -r requirements.txt -t .
```

3. Crete the s3 bucket.
```bash
sam-app$ aws s3 mb s3://BUCKET_NAME
```

4. To prepare the application for deployment, use the `sam package` command.

```bash
sam-app$ sam package \
    --output-template-file packaged.yaml \
    --s3-bucket BUCKET_NAME
```

5. Deploy the package

```bash
sam-app$ sam deploy \
    --template-file packaged.yaml \
    --stack-name aws-services-list \
    --capabilities CAPABILITY_IAM
```

6. After deployment is complete you can run the following command to retrieve the API Gateway Endpoint URL:

```bash
sam-app$ aws cloudformation describe-stacks \
    --stack-name aws-services-list \
    --query 'Stacks[].Outputs' \
    --output table
``` 

## Usage

- From above output, use the 'API Gateway endpoint URL' value.
- Use it in a browser or any http client.
- It will output the AWS services list with **region codes**

**To get the regions names:**
- Use query parameter `region_names=true` to get the real region names instead of codes


## Output format
With Region Codes:
```json
{
   "last_updated":"2019-10-29",
   "data":{
      "Alexa for Business":[
         "us-east-1"
      ],
      "Amazon API Gateway":[
         "ap-east-1",
         "ap-northeast-1",
         "ap-northeast-2",
         "ap-south-1",
         "ap-southeast-1",
         "ap-southeast-2",
         "ca-central-1",
         "cn-north-1",
         "cn-northwest-1",
         ...
         ...
      ],
      ...
      ...
   }
}
```

With Region Names:
```json
{
   "last_updated":"2019-10-29",
   "data":{
      "Alexa for Business":[
         "Northern Virginia"
      ],
      "Amazon API Gateway":[
         "AWS GovCloud (US-East)",
         "AWS GovCloud (US-West)",
         "Bahrain",
         "Beijing",
         "Frankfurt",
         "Hong Kong",
         "Ireland",
         "London",
         ...
         ...
      ],
      ...
      ...
   }
}
```

## Notes

These data are based on AWS's official [Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/).
This service provides the extracted data of the above page.

## Demo

* With region codes:  [https://aws-services.pubudu.dev/](https://aws-services.pubudu.dev).
* With region names:  [https://aws-services.pubudu.dev/?region_names=true](https://aws-services.pubudu.dev/?region_names=true).

# License

MIT License (MIT)
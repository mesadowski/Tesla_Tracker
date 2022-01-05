# Tesla_Tracker
Track your tesla using the Tesla API and AWS Lambda and DynamoDB

Set this up in the AWS Lambda console. You can trigger it periodically by setting an AWS Eventbridge trigger. You'll need to also create a
DynamoDB table, and enter the name of it and your Tesla user ID (email) in the environment variables for the Lambda. You need to use an 
IAM role for your Lambda that has the basic Lambda execution role, as well as the ability to write to your DynamoDB table and to read and write to Parameters Store. Building a zip file that you upload to AWS Lambda can be a bit tricky. You need to include the teslapy library in your zip file and if you don't get it right, it won't work. To authenticate to Tesla for the first time, follow instructions provided by https://github.com/tdorssers/TeslaPy. Run the code on his readme, and type in your Tesla user ID and password and get a URL that you can then use to get your first tokens. You can paste that (the whole JSON for all parameters) into AWS parameter store from the AWS Console, and subsequent token refreshes should be managed by teslapy.
For additional details see https://mikesml.com/2021/01/30/i-hacked-my-tesla-it-turned-out-to-be-a-bad-idea/ and https://mikesml.com/2021/12/30/tesla-hacking-with-aws-part-2-aws-lambda-dynamodb-and-parameter-store/

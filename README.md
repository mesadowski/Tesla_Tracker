# Tesla_Tracker
Track your tesla using the Tesla API and AWS Lambda and DynamoDB

Set this up in the AWS Lambda console. You can trigger it periodically by setting an AWS Eventbridge trigger. You'll need to also create a
DynamoDB table, and enter the name of it in the environment variables for the Lambda, and also add your Tesla web site credentials. You need to use an 
IAM role for your Lambda that has the basic Lambda execution role, as well as the ability to write to your DynamoDB table. The hardest part of this is 
building a zip file that you upload to AWS Lambda. You need to include the MyTesla and Requests libraries in your zip file and if you don't get it right, it won't work. 
For additional details see https://mikesml.com/2021/01/30/i-hacked-my-tesla-it-turned-out-to-be-a-bad-idea/

# Clone Repo and Build Docker Image
git clone https://github.com/iandow/opencv_aws_lambda
cd opencv_aws_lambda
docker build --tag=python-opencv-factory:latest .
docker run --rm -it -v $(pwd):/data python-opencv-factory cp /packages/cv2-python39.zip /data


# Lambda Layer Publish
ACCOUNT_ID=$(aws sts get-caller-identity | jq -r ".Account")
LAMBDA_LAYERS_BUCKET=lambda-layers-$ACCOUNT_ID
LAYER_NAME=cv2
aws s3 mb s3://$LAMBDA_LAYERS_BUCKET
aws s3 cp cv2-python39.zip s3://$LAMBDA_LAYERS_BUCKET
aws lambda publish-layer-version --layer-name $LAYER_NAME --description "Open CV" --content S3Bucket=$LAMBDA_LAYERS_BUCKET,S3Key=cv2-python39.zip --compatible-runtimes python3.9
LAYER=$(aws lambda list-layer-versions --layer-name $LAYER_NAME | jq -r '.LayerVersions[0].LayerVersionArn')

echo $LAYER

# Resource
https://github.com/iandow/opencv_aws_lambda
https://www.bigendiandata.com/2019-04-15-OpenCV_AWS_Lambda/
https://docs.aws.amazon.com/lambda/latest/dg/images-create.html

# Serverless ECR Deployments:
https://www.serverless.com/blog/container-support-for-lambda
https://dev.to/ajcwebdev/how-to-deploy-a-docker-container-on-aws-lambda-57gg
https://github.com/ajcwebdev/ajcwebdev-docker-lambda

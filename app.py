import boto3
import botocore.config
import json
from datetime import datetime 

def blog_gen_bedrock(blogtopic:str)->str:
    prompt=f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
    Assistant:[/INST]
    """
    body ={
        "prompt": prompt,
        "max_gen_len":512,
        "temperature":0.3,
        "top_p": 0.9
    }
    try:
        bedrock = boto3.client("bedrock-runtime", region="us-east-1",
                               config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3}))
        response = bedrock.invoke_model(body=json.dumps(body), modelId='meta.llama2-13b-chat-v1')
        response_content = response.get('body').read()
        response_data = json.loads(response_content)
        blog_details = response_data['generation']
        return blog_details
    except Exception as e:
        print(f"Error while generating the blog : {e}")
        return ""
    

def save_blog_s3(s3_key,s3_bucket,generate_blog):
    s3 =boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body=generate_blog)
        print("Code saved to s3")
    except Exception as e:
        print(f"Error while saving the code to s3 {e}")
    
def lambda_handler(event,context):
    event = json.loads(event['body'])
    blogtopic = event['blogtopic']
    generate_blog = blog_gen_bedrock(blogtopic=blogtopic)

    if generate_blog:
        current_time = datetime.now().strftime("%H%M%S")
        s3_key = f"blog-output/{current_time}.txt"
        s3_bucket = "bedrockblog"
        save_blog_s3(s3_key,s3_bucket,generate_blog)
    else:
        print("No blog was generated")
    
    return {
        'statusCode' : 200,
        'body' : json.dumps('Blog Generated!')
    }

# VideoSense — AI Video Assistant

VideoSense turns a YouTube link or uploaded video into a transcript, summary, action items, key facts, and questions. Users can also ask questions about the video.

## Architecture

The React UI calls two FastAPI APIs. SQS passes jobs to the ingestion, transcription, and summarization workers. S3 stores media and transcripts; DynamoDB stores job state; ChromaDB supports video chat. For AWS, the containers run on EC2 and use real S3, SQS, and DynamoDB. For local runs, LocalStack emulates those AWS services.

## Run locally

Requirements: Docker Desktop with Compose and a Mistral API key. A Sarvam key is optional and is only needed for Hindi transcription.

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your-mistral-api-key
SARVAM_API_KEY=your-sarvam-api-key
```

From the project root, run:

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
```

Open [http://localhost](http://localhost). The first run builds the containers and downloads the Whisper model. Stop the app with `Ctrl+C`; remove containers with:

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml down
```

Add `-v` to `down` only if you want to erase local jobs and indexes too.

## Deploy on AWS

1. From the project root, create the S3 bucket, DynamoDB table, SQS queues, and EC2 role:

   ```bash
   aws cloudformation deploy --template-file aws-resources.yml --stack-name videosense --capabilities CAPABILITY_NAMED_IAM --region ap-south-1
   aws cloudformation describe-stacks --stack-name videosense --query "Stacks[0].Outputs" --output table --region ap-south-1
   ```

2. Launch an Ubuntu EC2 instance, attach the `AppInstanceProfileName` from the outputs, and allow HTTP on port 80. Install Docker Engine and Compose, then clone this repository.

3. Create `.env` with `MISTRAL_API_KEY`, `AWS_REGION=ap-south-1`, and `JOBS_BUCKET` set to the `JobsBucketName` output. Start the app:

   ```bash
   docker compose up -d --build
   ```

Open the instance’s public IP over HTTP. EC2’s role provides AWS credentials; do not put AWS access keys in `.env`.

## Project folders

- `services/` — APIs and processing workers
- `shared/` — AWS storage, queue, and job helpers
- `UI/` — React frontend and Nginx proxy
- `tests/` — backend tests
- `aws-resources.yml` — AWS data services and EC2 role

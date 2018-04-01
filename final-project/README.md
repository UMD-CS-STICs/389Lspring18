# Final Project

### Overview

The goal of the final project is for all of you to build some kind of meaningful project that proves your AWS skillset to employers.

It should also help you develop experience planning the architecture of a cloud system, and interconnecting different AWS services to build a project in a scalable fashion.

We'll be discussing this project on 3/16, however you are more than welcome to start early.

### Requirements

This project is meant to be extremely open-ended. There are really just two requirements:

1. You must use **at least three** AWS services.
2. **At least one** of those services must have not been covered in class.

Some AWS services are not going to be eligible to be counted towards the above requirement. These services are either required for almost any project, or are not going to be substantive in their implementation. For now, this list includes:
- IAM
- CloudWatch

The list of services that **cannot be counted** towards the second requirement are:
- S3
- CloudFront
- EC2
- SQS
- ALBs
- Lambda
- API Gateway
- DynamoDB

The following services will be covered, but you are welcome to count them towards the 2nd requirement because you will need to learn them on your own prior to when they are covered in class.
- ECS
- Elasticsearch Service
- CloudFormation

### Deliverables

Here are the major deadlines that you should keep in mind:

| Deliverable    	| Due Date    | Percent             |
| ----------------- | ----------- | ------------------- |
| [Proposal](https://piazza.com/class/jcsfmcmvvp46ju?cid=92)       	| 4/1        | 10%                 |
| Checkpoint 1     	| 4/13        | 10%                  |
| Checkpoint 2     	| 4/27        | 10%                  |
| Codebase       	| 5/11        | 30% (10% per service) |
| Video Demo     	| 5/11        | 10%                 |
| In-person Demo 	| 5/11 - 5/17     | 10%                 |
| (Creativity) 		| N/A    	  | 20%                 |

You can get an extra 10% per service that you use, up to 30% extra credit. You can also get up to an extra 10% for load testing your app (f.e. with [Bees with Machine Guns](https://github.com/newsapps/beeswithmachineguns)) and including this in your video demo.

All deliverables are due by 11:59:59PM on the above due date.

#### Proposal

Your proposal will be structured as a slide deck. It should touch on at least the following topics:
- What do you want to build?
- How will it work from a user's perspective?
- What services will you use to build it and how will those services work together?
- How will your service scale?
- If you need hardware, what do you need and how will you get it?
- If you need a data set, where will you get it?

See [this slide deck](http://slides.com/colinking/example-proposal) for an example of what a proposal may look like.

Submit a link to your proposal slides (Dropbox, slides.com, etc.) as a follow-up discussion post to [this Piazza post](https://piazza.com/class/jcsfmcmvvp46ju?cid=92).

To create an architecture diagram, I would recommend either [Draw.io](https://www.draw.io/?splash=0&libs=aws2) or [Cloudcraft](https://cloudcraft.co/app).

A sign-up sheet will be released later this semester to sign up for a time slot to present your proposal to the facilitators. You'll have up to 10 minutes to run through your presentation, then the remaining 5 minutes will be for questions and feedback. Presentations will happen in the Sandbox makerspace (CSIC 3107).

#### Checkpoint

Every two weeks between when the proposal is due and when the demo is due, you will submit a checkpoint to update the facilitators on your progress and any roadblocks you've run into.

You will need to submit a write-up that includes:
- An overview of the progress you have made so far.
- The remaining work to be completed.
- A list of changes you have made to your project since your last proposal/checkpoint.
- Problems that you have encountered so far and how you have addressed them.
- A link to your updated GitHub codebase. Make sure to include a `README.md`.

You can submit the checkpoints to the submit server.

#### Codebase

This project is meant to be released publicly so that employers can look over what you have built. Therefore, you will need to upload all work to a public GitHub repository. There will be a Piazza post later this semester where you can submit the link to your GitHub repo.

You will also need to include a README file with your GitHub repo. It should contain an overview of the project, links to your public YouTube video, your architecture diagram, an overview of your API (if you have one), and [the "cmsc389l" tag](https://github.com/topics/cmsc389l).

Your repo should contain everything that someone would need to recreate your application. If there are settings you had to configure in the Management Console or elsewhere, add some high-level notes of those steps in your README. For example, if you had write your own IAM policies, or configure the Skills Kit then you should include those JSON files in your repo.

#### Video Demo

You will need to record a video demo of your application (at least 2-3 minutes).

Make sure your demo:
- Includes a high-level overview and demonstration of your project
- Shows your application in action
- Walks through your application architecture diagram
- Briefly discusses how you handled scalability concerns
- A description of the hardest problem you encountered and your solution

To record parts of your demo, you can use [Loom](https://www.useloom.com?ref=160191). There are a number of simple video editing tools out there, such as iMovie, that you can use to splice together clips to form your demo. (Have a recommendation for editing software? Post it on Piazza!)

I encourage you to make this video as professional as reasonably possible! After all, employers will see this.

#### In-person Demo

You will need to give an in-person demo of your project to the course facilitators. The sign-up sheet will be posted later in the semester.

We'll try to ask the kind of questions that we would expect employers to ask, if you were to show them your project.

### Example Project: Alexa Chess App

{{ 'http://slides.com/colinking/example-proposal' | iframely }}

#### Other Project Ideas

There are a lot of really interesting services that you can use to build fun projects! Here are some more high-level ideas:

- [AWS IoT](https://aws.amazon.com/iot/): Build something cool with sensor data! Check out the [Programmable IoT Dash Buttons](https://aws.amazon.com/iotbutton/). Or walk in to the Sandbox and chat with any of the managers about the hardware available to you.
- [AWS Lex](https://aws.amazon.com/lex/): Build a chat-based assistant on Slack/Messenger/etc. (Brownie points if you make a sassy one, like [Poncho](https://poncho.is/): [article](https://chatbotsmagazine.com/think-differently-when-building-bots-5093ddba5a56))
- Big Data: Process Twitter data in real-time with the [Kinesis Streams](https://blog.insightdatascience.com/getting-started-with-aws-serverless-architecture-tutorial-on-kinesis-and-dynamodb-using-twitter-38a1352ca16d), or build an AWS MapReduce job to create a data visualization off of a [Wikipedia data dump](https://dumps.wikimedia.org/)
- [AWS GameLift](https://console.aws.amazon.com/gamelift/home?region=us-east-1#/): Build a multiplayer game and host it in the cloud!

That only scratches the surface of the number of ideas you could run with. Here a picture of all of the services currently available on AWS!

![Lots of AWS Services](../../media/final-project/services.png)

### Hardware

The [Sandbox](sandbox.cs.umd.edu) (new CS makerspace) has a lot of hardware that can be used for projects, along with guidance and advice! If you haven't worked with hardware before, this is a great opportunity to get started and try it out. If you haven't been to Sandbox before, it is located in CSIC 3107, just on your right before you walk across the bridge to AVW.

If you are looking for a specific piece of hardware, make a post on Piazza! Someone may be able to lend it to you.

### Competitions

There are a handful of opportunities to submit your project into competitions and compete for prizes! Here are a few:

- [Online hackathons](https://devpost.com/hackathons?utf8=%E2%9C%93&search=&challenge_type=online&sort_by=Submission+Deadline)
- [Or in-person hackathons over the weekends!](https://www.facebook.com/groups/hackersofmaryland/) (Check Terrapin Hackers. If we have a bus then you don't need to be admitted, just hop on!)

### Questions

> Are we limited to any language or can we use any language of our choice?

You are welcome to use whichever language of your choice. Though keep in mind that Python would be the preferred choice, since all facilitators are experienced with the language and the AWS libraries, so we'll be able to help out more.

If you choose another language, make sure to address this in your proposal.

> Can we work in teams or do we need to work on our own?

I heavily encourage you to work as a single-person team, since building a full project on your own is much more meaningful to employers than team projects where your contributions are harder to pinpoint.

However, if there is a situation where two students really want to work together, then you can go for it. I will expect the scope of the project to be double in size to account for two teammates working together. **If you want to work on a team project, shoot me an email soon** with an overview of what you want to build, so that I can get back to you ASAP on whether it is the right scope for a two-person team.

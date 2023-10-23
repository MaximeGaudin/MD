## Log
- Start: 8h34
- End of design/conception phase: 9h20
- End of coding 12h40
  ![[MadKudu_-_Work_sample_-_Software_Engineer_.pdf]]
## Discovery
- Large CSV files
    - How large? Currently, 150Mb
- S3 bucket
- Serve Data Analyses:
    - Which one? **Cf. Examples**
    - By email? From the product? Via CS?
        - **Via an interface + Machine 2 Machine format**
- Who will write the data analyses:
    - Expert users (i.e. data eng.)?
    - Intermediate (i.e. "regular" devs)?
    - Sales team?
- "We lost patience processing these files manually"
    - For how long?
    - How long does it take?
- Dedicated program:
    - Because it's a case or is there a business reason for that?
- Expected 2h to 4h or work
- Explicit Goals:
    - Building a working MVP
    - Make your project as understandable as possible (with or without docs)
    - Write a design document on how you would:
        - Industrialize it
        - Deploy it to production
        - make it recurring
        - Monitor the runs
        - "etc."
- Business Goals
    - Download and process a file from a S3 Bucket
    - Given a year-month parameter, process the specified range of data and output "some" data analysis
    - On top of outputing customer actionable data, make the data available via DB, file, API, etc.
    - The retrieving & processing should be automatic (but can be triggered manually)
    - Analyses examples:
        - number of events per year/month/day
        - most active users
        - most active companies
        - "Feel free to share your own suggestions!"
- Material
    - s3://work-sample-mk/2021/04/events.csv
    - us-west-2

## Architecture Design

- Language choices:
    - Front: Vuejs, because it's my goto front-end language. However, knowing that MD uses React, in this context, I would have gone with React.
    - Back: Usually, Kotlin is my goto language but Python ecosystem is so rich for data analysis, in particular with Pandas, that I can see the time gain at every step of the way. So Python it is.
    - DB: I decided to use a DB instead of a file to store the input & analysis results. This way, if we decide to migrate our process and/or stack at some point (e.g. go from Python to Nodejs or switch from Postgres to Redshift), everything will be there, clean and waiting to be copied to the new DB. It's also a great way to store, in the same place, the input data, the output data, the logs, and the configuration. Finally, I chose PostgreSQL because I am very used to it, support JSONb format nativelly, GEO data easily with PostGIS and will be able to support very large quantities of data before we need to think of a migration.
- Architecture:
    - Super classic web archi:
        - Nginx proxing requests to our backend and front-end
        - Everything goes into a docker so that it can be deployed super quickly, locally for testing of directly on AWS
- Name: Because it needs a name, not sure why but I went with... Moonshine !
    - Did I generate the logo on Dall-E? Maybe.
# Architecture

Travel Vista is organized as a portfolio version of the WIL capstone project.

## Main Layers

1. Flask application
   - Browser dashboard at `/`
   - JSON APIs for summary metrics, destination ranking, recommendations, secure insert simulation, and VR engagement scoring

2. Analytics layer
   - Loads local CSV extracts
   - Computes destination performance, region revenue, activity mix, and platform summary metrics

3. Recommendation layer
   - Uses TF-IDF text vectors over destination names, world wonders, package options, transport modes, and dynamic tags
   - Scores user search intent with cosine similarity

4. Security layer
   - Demonstrates AES encryption for sensitive payloads
   - Reads keys from environment variables instead of hardcoding credentials

5. Data engineering scripts
   - S3 upload script
   - Async PostgreSQL loader
   - PySpark visit-processing pipeline
   - Elasticsearch indexing script

## Original WIL Source Used

The cleaned repository was rebuilt from:

- `TRAVEL VISTA - MID TERM - WEEK 6/Codes`
- `Week 6 deliverables/travel_insights_dashboard`
- `Week 12 deliverables`
- `TRAVEL VISTA - MID TERM - WEEK 6/Mid_Term_Presentation.pptx`

Local virtual environments, personal career documents, videos, and hardcoded secrets were intentionally excluded.


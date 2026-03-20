-- Pull all patents assigned to OpenAI from Google BigQuery's public patent dataset.
-- Dataset: patents-public-data.patents.publications
-- Run this in BigQuery console or via the BigQuery API.
-- Returns ~106 results; see README for how we cleaned to 62.

SELECT
    publication_number,
    application_number,
    country_code,
    filing_date,
    publication_date,
    grant_date,
    title_localized,
    abstract_localized,
    inventor,
    assignee_harmonized,
    cpc
FROM `patents-public-data.patents.publications`
WHERE EXISTS (
    SELECT 1 FROM UNNEST(assignee_harmonized) a
    WHERE LOWER(a.name) LIKE '%openai%'
)
ORDER BY publication_date DESC

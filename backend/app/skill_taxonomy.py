SKILL_TAXONOMY = {
    "languages": [
        "python",
        "sql",
        "bash",
        "javascript",
        "typescript",
        "java",
    ],
    "ai_ml": [
        "machine learning",
        "deep learning",
        "nlp",
        "computer vision",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "pandas",
        "numpy",
        "model evaluation",
        "feature engineering",
    ],
    "genai": [
        "llm",
        "rag",
        "prompt engineering",
        "embeddings",
        "vector database",
        "langchain",
        "openai",
    ],
    "backend": [
        "fastapi",
        "rest api",
        "authentication",
        "microservices",
        "pydantic",
    ],
    "data_engineering": [
        "postgresql",
        "mysql",
        "spark",
        "airflow",
        "prefect",
        "dbt",
        "etl",
        "elt",
        "data pipeline",
    ],
    "mlops_devops": [
        "docker",
        "kubernetes",
        "github actions",
        "ci/cd",
        "mlflow",
        "terraform",
        "prometheus",
        "grafana",
        "linux",
    ],
    "cloud": [
        "aws",
        "azure",
        "gcp",
        "s3",
        "lambda",
        "cloud run",
        "app service",
    ],
}


def all_skills() -> list[str]:
    skills: list[str] = []
    for group in SKILL_TAXONOMY.values():
        skills.extend(group)
    return sorted(set(skills))


"""Módulo principal da aplicação."""

from fastapi import FastAPI
from database import Base, engine
from crud.ingredientes import router as ingredientes_router
from crud.receitas import router as receitas_router
from status.health import router as health_router
from prometheus_fastapi_instrumentator import Instrumentator

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

if engine is not None:
    Base.metadata.create_all(bind=engine)

app = FastAPI()

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "python-recipe-api"})
    )
)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

app.include_router(ingredientes_router)
app.include_router(receitas_router)
app.include_router(health_router)

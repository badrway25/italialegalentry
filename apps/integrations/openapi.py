"""Hand-written OpenAPI 3.1 description of the internal API v1 (ADR-011). Served at /api/v1/schema/."""

from __future__ import annotations

ERROR_SCHEMA = {
    "type": "object",
    "required": ["error"],
    "properties": {
        "error": {
            "type": "object",
            "required": ["code", "message", "request_id"],
            "properties": {
                "code": {
                    "type": "string",
                    "enum": [
                        "unauthorized",
                        "insufficient_scope",
                        "rate_limited",
                        "not_found",
                        "method_not_allowed",
                        "invalid_json",
                        "invalid_parameter",
                        "event_cancelled",
                        "unknown_system",
                        "malformed_headers",
                        "timestamp_out_of_range",
                        "secret_not_configured",
                        "invalid_signature",
                        "replay",
                        "payload_too_large",
                    ],
                },
                "message": {"type": "string"},
                "request_id": {"type": "string"},
            },
        }
    },
}

EVENT_SCHEMA = {
    "type": "object",
    "required": ["uuid", "event_type", "occurred_at", "status", "data"],
    "properties": {
        "uuid": {"type": "string", "format": "uuid"},
        "event_type": {"type": "string", "examples": ["enquiries.company_needs.created"]},
        "occurred_at": {"type": "string", "format": "date-time"},
        "status": {"type": "string", "enum": ["queued", "delivered", "failed", "cancelled"]},
        "attempts": {"type": "integer"},
        "object": {
            "type": ["object", "null"],
            "properties": {"type": {"type": "string"}, "id": {"type": "string"}},
        },
        "data": {
            "type": "object",
            "description": "Minimal payload: identifiers, timestamps and closed-vocabulary codes only. "
            "Never personal data or free text (contract §6).",
            "additionalProperties": {"type": ["string", "integer", "number", "boolean", "null"]},
        },
        "created_at": {"type": "string", "format": "date-time"},
        "delivered_at": {"type": ["string", "null"], "format": "date-time"},
        "acknowledged_at": {"type": ["string", "null"], "format": "date-time"},
    },
}

_ERROR_RESPONSES = {
    "401": {
        "description": "Missing, invalid, inactive or expired API key.",
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
    },
    "403": {
        "description": "Key lacks the required scope.",
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
    },
    "429": {
        "description": "Throttled (per API key).",
        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
    },
}

SCHEMA: dict = {
    "openapi": "3.1.0",
    "info": {
        "title": "Italy Legal Entry™ — Integration API",
        "version": "1.0.0",
        "summary": "CRM-ready boundary: outbound event pull/ack, inbound webhooks, health.",
        "description": "Internal, versioned API (ADR-011). Every response carries a request_id; errors use "
        "one envelope. See docs/CRM_INTEGRATION_CONTRACT.md.",
        "contact": {"name": "AGAMI — Dialogo Giuridico Interculturale APS", "email": "contact@agamieuromed.org"},
    },
    "servers": [{"url": "/api/v1"}],
    "security": [{"bearerAuth": []}],
    "paths": {
        "/health/": {
            "get": {
                "operationId": "health",
                "summary": "Liveness of the API layer (no authentication).",
                "security": [],
                "responses": {
                    "200": {
                        "description": "API is up.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "status": {"type": "string", "const": "ok"},
                                                "version": {"type": "string", "const": "v1"},
                                                "time": {"type": "string", "format": "date-time"},
                                            },
                                        },
                                        "request_id": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                },
            }
        },
        "/events/": {
            "get": {
                "operationId": "listEvents",
                "summary": "List outbound events visible to the authenticated key (scope events:read).",
                "parameters": [
                    {
                        "name": "status",
                        "in": "query",
                        "schema": {
                            "type": "string",
                            "enum": ["queued", "delivered", "failed", "all"],
                            "default": "queued",
                        },
                    },
                    {
                        "name": "since",
                        "in": "query",
                        "description": "ISO-8601 date-time; only events created at or after this instant.",
                        "schema": {"type": "string", "format": "date-time"},
                    },
                    {"name": "event_type", "in": "query", "schema": {"type": "string"}},
                    {
                        "name": "after",
                        "in": "query",
                        "description": "Keyset cursor: the `next_after` value of the previous page.",
                        "schema": {"type": "integer"},
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "schema": {"type": "integer", "minimum": 1, "maximum": 200, "default": 50},
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Page of events ordered by creation (ascending id).",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {"type": "array", "items": {"$ref": "#/components/schemas/Event"}},
                                        "pagination": {
                                            "type": "object",
                                            "properties": {
                                                "limit": {"type": "integer"},
                                                "has_more": {"type": "boolean"},
                                                "next_after": {"type": ["integer", "null"]},
                                            },
                                        },
                                        "request_id": {"type": "string"},
                                    },
                                }
                            }
                        },
                    },
                    "400": {
                        "description": "Invalid query parameter.",
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
                    },
                    **_ERROR_RESPONSES,
                },
            }
        },
        "/events/{uuid}/ack/": {
            "post": {
                "operationId": "ackEvent",
                "summary": "Acknowledge an event (idempotent; scope events:ack).",
                "parameters": [
                    {"name": "uuid", "in": "path", "required": True, "schema": {"type": "string", "format": "uuid"}}
                ],
                "responses": {
                    "200": {
                        "description": "Event marked delivered (or already acknowledged — same response).",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {"$ref": "#/components/schemas/Event"},
                                        "request_id": {"type": "string"},
                                    },
                                }
                            }
                        },
                    },
                    "404": {
                        "description": "Unknown event or not visible to this key.",
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
                    },
                    "409": {
                        "description": "Event was cancelled.",
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
                    },
                    **_ERROR_RESPONSES,
                },
            }
        },
        "/webhooks/{system}/": {
            "post": {
                "operationId": "inboundWebhook",
                "summary": "Receive a signed webhook from a registered external system.",
                "security": [{"hmacSignature": []}],
                "parameters": [
                    {"name": "system", "in": "path", "required": True, "schema": {"type": "string"}},
                    {
                        "name": "X-Signature",
                        "in": "header",
                        "required": True,
                        "schema": {"type": "string"},
                        "description": "sha256=HMAC_SHA256(secret, timestamp + '.' + nonce + '.' + raw_body)",
                    },
                    {
                        "name": "X-Timestamp",
                        "in": "header",
                        "required": True,
                        "schema": {"type": "string"},
                        "description": "Unix seconds; ±300 s tolerance.",
                    },
                    {
                        "name": "X-Nonce",
                        "in": "header",
                        "required": True,
                        "schema": {"type": "string"},
                        "description": "8–64 chars, unique per system (replay protection).",
                    },
                ],
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object"}}}},
                "responses": {
                    "202": {
                        "description": "Accepted and logged.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "data": {
                                            "type": "object",
                                            "properties": {
                                                "accepted": {"type": "boolean"},
                                                "log_id": {"type": "integer"},
                                            },
                                        },
                                        "request_id": {"type": "string"},
                                    },
                                }
                            }
                        },
                    },
                    "400": {
                        "description": "Invalid JSON body.",
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
                    },
                    "401": {
                        "description": "Unknown system, bad signature, stale timestamp or replayed nonce.",
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
                    },
                    "413": {
                        "description": "Body too large.",
                        "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}},
                    },
                },
            }
        },
        "/schema/": {
            "get": {
                "operationId": "schema",
                "summary": "This document.",
                "security": [],
                "responses": {
                    "200": {
                        "description": "OpenAPI 3.1 JSON.",
                        "content": {"application/json": {"schema": {"type": "object"}}},
                    }
                },
            }
        },
    },
    "components": {
        "securitySchemes": {
            "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "ile_<prefix>_<secret>"},
            "hmacSignature": {"type": "apiKey", "in": "header", "name": "X-Signature"},
        },
        "schemas": {"Error": ERROR_SCHEMA, "Event": EVENT_SCHEMA},
    },
}

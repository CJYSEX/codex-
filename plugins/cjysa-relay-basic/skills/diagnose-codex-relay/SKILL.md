---
name: diagnose-codex-relay
description: Diagnose Codex relay connectivity and compatibility without exposing credentials. Use when a user asks to test a custom API base URL, list available models, verify the Responses API or SSE streaming, investigate first-token latency, or check whether web search, image generation, and function calling are available through a relay.
---

# Diagnose Codex Relay

Diagnose one layer at a time and report evidence instead of assuming a capability works.

## Safety

- Never print, quote, save, or commit an API key.
- Redact authorization headers, query tokens, cookies, passwords, and signed URLs.
- Prefer read-only health checks and minimal requests.
- Ask before running sustained concurrency or bandwidth tests.
- Do not modify Codex configuration unless the user explicitly asks for a change.

## Workflow

1. Identify the configured API base URL without displaying its secret.
2. Check DNS resolution, TLS validity, and basic HTTP reachability.
3. Request `/v1/models` and record status, elapsed time, and returned model IDs.
4. Send a minimal synchronous request to the requested model.
5. Test `/v1/responses` separately from Chat Completions.
6. Test SSE streaming and measure time to the first meaningful event.
7. Test function calling, web search, or image generation only when the user requests it.
8. Separate client, reverse-proxy, relay, and upstream latency when diagnosing delays.
9. Report results as passed, failed, unsupported, or not tested.

## Evidence

For each test, record:

- Endpoint category, without secret query parameters.
- HTTP status or transport error.
- Total elapsed time and first-event latency where applicable.
- Whether valid response content was received.
- Whether the result proves the claimed capability.

Do not claim web search succeeded without a returned search result or source. Do not claim image generation succeeded without a native image result or generated artifact.

## Diagnosis Rules

- `/v1/models` succeeding proves authentication and catalog access only.
- A synchronous response does not prove SSE streaming works.
- Chat Completions success does not prove the Responses API works.
- A model name appearing in the catalog does not prove tool support.
- Compare direct relay access with the public domain when isolating reverse-proxy delay.
- When context length affects latency, compare short and long prompts separately.

## Output

Return a compact table of tests, followed by:

- The most likely fault layer.
- Tests that were not performed.
- The smallest next action.
- A reminder to rotate any credential accidentally exposed during testing.

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-29

### Added

- Impersonate button on the user page and column in the user list, for superusers.
- Impersonation through django-impersonate, limited to superusers impersonating
  active non-superusers.
- Start and stop accept POST only.
- Top bar banner with a Stop button while impersonating.
- Compatibility with NetBox 4.7.

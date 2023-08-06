# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2022-09-06

### Added
- INI is now iterable (yields section names), and has a keys method for iterating over keys in a section.

### Fixed
- Files which do not end in a line separator can now be added to without mangling the file by omitting it
  after the last original entry.

## [0.2.0] - 2022-04-04 

### Changed
- The file argument to the `INI` class is now optional, to allow the creation of new ini files.

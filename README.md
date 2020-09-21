# XL Release Telnet Plugin v0.1.0

[![Build Status][xlr-telnet-plugin-travis-image]][xlr-telnet-plugin-travis-url]
[![License: MIT][xlr-telnet-plugin-license-image]][xlr-telnet-plugin-license-url]
![Github All Releases][xlr-telnet-plugin-downloads-image]

[xlr-telnet-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-telnet-plugin.svg?branch=master
[xlr-telnet-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-telnet-plugin
[xlr-telnet-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-telnet-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-telnet-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-telnet-plugin/total.svg

## Preface

**This is a pre-release plugin that is still undergoing development.**

This is a 'See It Work' plugin, meaning it has been enhanced to include functionality that makes it easy to spin up and configure a dockerized version of the XebiaLabs platform with this plugin installed. Using the provided test data, you can then try out the plugin features. This is useful for familiarizing yourself with the plugin functionality, for demonstrations, testing and for further plugin development.

This document describes the functionality provided by the XL Release Telnet plugin. 
  
See the [XL Release reference manual](https://docs.xebialabs.com/xl-release) for background information on XL Release and release automation concepts.  

## Overview

This plugin provides a way to run simple command sequences on a telnet server. At this point, its capabilites are quite unsophisicated.

The plugin adds a new server type named 'Telnet Server'. Currently, there is a single new task type name 'Run Commands'.

## Requirements

*XL Release version 9.0+
*This plugin has been tested on version 9.7 as well

## Installation

* Copy the latest JAR file from the [releases page](https://github.com/xebialabs-community/xlr-telnet-plugin/releases) into the `XL_RELEASE_SERVER/plugins/__local__` directory.
* Restart the XL Release server.

## Usage

### Configure the Telnet Server

![AddServer](images/AddServer.png)

Add a new Telnet Server on the Settings -> Shared Configration page.

## References

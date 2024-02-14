# Converter for the OrgaTalk LANparty Database


## Supported input formats

* [DOTLAN Intranet](https://intranet.dotlan.net/) SQL dump
* [LANsuite](https://github.com/lansuite/lansuite) XML


## Usage

* [Install Rye](https://rye-up.com/guide/installation/)
* Clone repository: `git clone https://github.com/orgatalk/lanpartydb-tools.git`
* Enter converter path: `cd lanpartydb-tools/converter`
* Setup project including dependencies: `rye sync`
* Run converter:
  * For DOTLAN: `rye run convert-dotlan-sql --base-url 'https://www.lanparty.example' --output-path output events-and-locations.sql`
    * Export tables `events` and `event_location` (both structure and
      data, without compression) from the DOTLAN "Support Tools"
  * For LANsuite: `rye run convert-lansuite-xml --output-path output infos.xml`
    * The XML document with parties is publicly available at
      `https://www.yourparty.example/ext_inc/party_infos/infos.xml`.


## License

MIT


## Author

Jochen Kupperschmidt

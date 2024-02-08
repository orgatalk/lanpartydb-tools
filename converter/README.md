# Converter for the OrgaTalk LANparty Database


## Supported input formats

* [DOTLAN Intranet](https://intranet.dotlan.net/) SQL dump


## Usage

* [Install Rye](https://rye-up.com/guide/installation/)
* Clone repository: `git clone https://github.com/orgatalk/lanpartydb-tools.git`
* Enter converter path: `cd lanpartydb-tools/converter`
* Setup project including dependencies: `rye sync`
* Run converter:
  * For DOTLAN: `rye run convert-dotlan-sql --base-url 'https://www.lanparty.example' --output-path build events-and-locations.sql`


## License

MIT


## Author

Jochen Kupperschmidt

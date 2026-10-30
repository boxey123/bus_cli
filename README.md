# Bus Stop Finder

**Status**: In progress.
Stop data comes from a snapshot of the NaPTAN dataset taken on the 30/10/2026, so recent changes may not be reflected. A stop that has been removed or deactivated can still appear in results. A stop showing "No services found" may genuinely have no services, or may be one of these stops that has been removed or deactivated, and the live API no longer returns data for. To refresh the data you can download a new Edinburgh and the Lothians filtered snapshot from the NaPTAN dataset with the `fetch_naptan.py` script.

A Python command-line tool for finding bus stops and listing the services near an Edinburgh and the Lothians postcode.

You enter a postcode and search radius and it will list all active stops within that radius sorted by nearest first.

## How it works

1. The postcode that has been entered is sent to the postcodes.io Scotland endpoint where it returns the longitude and latitude of the provided postcode.
2. A radius is provided by the user and a bounding box is then created around the coordinate of the postcode.
3. The bounding box is then sent to the [City of Edinburgh Council Bustracker Open API](https://www.edinburghtraveltracker.com/), which returns the stops inside of it.
4. Each stop is searched for within a local copy (saved 30/10/2026) of the NaPTAN dataset filtered to Edinburgh and the Lothians to get the status, stop type and bearing of the stop.
5. Stops that are not for buses (e.g. taxi ranks), inactive, missing from the dataset or further away than the radius (measured with the haversine formula) are dropped. The remaining stops are displayed, sorted by the nearest first.

## Getting started

Requires Python 3.10 or newer.

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and add your Bus Tracker API key (register with the City of Edinburgh Council to get one).
3. Run `python main.py` from the project folder.

The repo includes a NaPTAN snapshot so it works out of the box. To refresh it run `python fetch_naptan.py` (needs internet access).

## Examples

Bearing is the direction buses travel from the stop.

### Example 1 - Apple Edinburgh

```
$ python main.py
Enter a postcode: EH2 2AN
Enter a radius in meters: 50

Services for Princes Street (Waverley Steps) (E)
  Service Name: 101, Operator: HOU, Service Reference: HOU 101 b
  Service Name: 101a, Operator: HOU, Service Reference: HOU 101a b
  Service Name: 16, Operator: LOTH, Service Reference: LOTH 16 a
  Service Name: 25, Operator: LOTH, Service Reference: LOB 25 b a
  Service Name: N16, Operator: LOTH, Service Reference: LOB N16 e a
  Service Name: N25, Operator: LOTH, Service Reference: LOB N25 c a
  Service Name: X39, Operator: MCG_Fleet, Service Reference: MESC X39

Services for Princes Street (Waverley Steps) (W)
  Service Name: 1, Operator: LOTH, Service Reference: LOB 1 a a
  Service Name: 15, Operator: LOTH, Service Reference: LOB 15 a g
  Service Name: 16, Operator: LOTH, Service Reference: LOTH 16 a
  Service Name: 25, Operator: LOTH, Service Reference: LOB 25 b a
  Service Name: 34, Operator: LOTH, Service Reference: LOB 34 c b
  Service Name: 4, Operator: LOTH, Service Reference: LOB 4 b e
  Service Name: N1, Operator: LOTH, Service Reference: LOTH N1 a
  Service Name: N107, Operator: LOTH, Service Reference: ECBU  N107 d
  Service Name: N11, Operator: LOTH, Service Reference: LOB N11 c
  Service Name: N113, Operator: LOTH, Service Reference: East  N113 b
  Service Name: N124, Operator: LOTH, Service Reference: ECBU  N124 c
  Service Name: N16, Operator: LOTH, Service Reference: LOB N16 e a
  Service Name: N25, Operator: LOTH, Service Reference: LOB N25 c a
  Service Name: N26, Operator: LOTH, Service Reference: LOTH N26 c
  Service Name: N3, Operator: LOTH, Service Reference: LOTH N3 a a
  Service Name: N30, Operator: LOTH, Service Reference: LOB N30 d h
  Service Name: N31, Operator: LOTH, Service Reference: LOTH N31 a e
  Service Name: N44, Operator: LOTH, Service Reference: LOB N44 b e
  Service Name: X26, Operator: LOTH, Service Reference: LOTH X26 b
  Service Name: X29, Operator: LOTH, Service Reference: LOB X29 b a

Services for Princes Street (Waverley Steps) (W)
  Service Name: 106, Operator: LOTH, Service Reference: ECBU 106 j
  Service Name: 19, Operator: LOTH, Service Reference: LOTH 19 b
  Service Name: 29, Operator: LOTH, Service Reference: LOTH 29 b a
  Service Name: 37, Operator: LOTH, Service Reference: LOTH 37 c a
  Service Name: N18, Operator: NELB, Service Reference: NELB N18 b
  Service Name: N28, Operator: NELB, Service Reference: NELB N28 b a
  Service Name: N37, Operator: LOTH, Service Reference: LOB N37 c f
  Service Name: N43, Operator: NELB, Service Reference: NELB N43 c
  Service Name: X37, Operator: LOTH, Service Reference: LOTH X37 a
  Service Name: X39, Operator: MCG_Fleet, Service Reference: MESC X39
  Service Name: X6, Operator: LOTH, Service Reference: ECBU  X6 h

Services for Princes Street (Waverley Steps) (E)
  Service Name: 15, Operator: LOTH, Service Reference: LOB 15 a g
  Service Name: 26, Operator: LOTH, Service Reference: LOTH 26 c
  Service Name: 44, Operator: LOTH, Service Reference: LOB 44 c j
  Service Name: N107, Operator: LOTH, Service Reference: ECBU  N107 d
  Service Name: N113, Operator: LOTH, Service Reference: East  N113 b
  Service Name: N124, Operator: LOTH, Service Reference: ECBU  N124 c
  Service Name: N26, Operator: LOTH, Service Reference: LOTH N26 c
  Service Name: N43, Operator: NELB, Service Reference: NELB N43 c
  Service Name: X26, Operator: LOTH, Service Reference: LOTH X26 b

Bus stop locations: Data provided by City of Edinburgh Council
```

### Example 2 - Our lady of Loretto and St Michael Catholic Church, Musselburgh

```
$ python main.py
Enter a postcode: EH21 7AJ
Enter a radius in meters: 75

Services for Newbigging (S)
  Service Name: 108, Operator: DPC, Service Reference: DPC 108 b
  Service Name: 111, Operator: DPC, Service Reference: DPC 111 b
  Service Name: 140, Operator: LOTH, Service Reference: ECBU  140 e
  Service Name: 141, Operator: LOTH, Service Reference: ECBU 141
  Service Name: 26, Operator: LOTH, Service Reference: LOTH 26 c
  Service Name: 44, Operator: LOTH, Service Reference: LOB 44 c j
  Service Name: 48, Operator: LOTH, Service Reference: LOTH 48 b a
  Service Name: N26, Operator: LOTH, Service Reference: LOTH N26 c
  Service Name: X11, Operator: DPC, Service Reference: DPC X11
  Service Name: X26, Operator: LOTH, Service Reference: LOTH X26 b
  Service Name: X4, Operator: LOTH, Service Reference: ECBU X4 c

Services for Newbigging (N)
  Service Name: 108, Operator: DPC, Service Reference: DPC 108 b
  Service Name: 111, Operator: DPC, Service Reference: DPC 111 b
  Service Name: 140, Operator: LOTH, Service Reference: ECBU  140 e
  Service Name: 141, Operator: LOTH, Service Reference: ECBU 141
  Service Name: 26, Operator: LOTH, Service Reference: LOTH 26 c
  Service Name: 44, Operator: LOTH, Service Reference: LOB 44 c j
  Service Name: 48, Operator: LOTH, Service Reference: LOTH 48 b a
  Service Name: N26, Operator: LOTH, Service Reference: LOTH N26 c
  Service Name: X11, Operator: DPC, Service Reference: DPC X11
  Service Name: X26, Operator: LOTH, Service Reference: LOTH X26 b
  Service Name: X4, Operator: LOTH, Service Reference: ECBU X4 c

Bus stop locations: Data provided by City of Edinburgh Council
```

## Credits and data sources

This is an independent student project. It is not affiliated with or endorsed by the City of Edinburgh Council, the Department for Transport or postcodes.io.

- **[City of Edinburgh Council Bustracker Open API](https://www.edinburghtraveltracker.com/)**: stop locations.
  Data provided by City of Edinburgh Council. Used under the [API licence and terms of use](https://www.edinburghtraveltracker.com/resources/docs/api_licence_and_terms_of_use.pdf).
- **NaPTAN** (National Public Transport Access Nodes), Department for Transport: stop status, type and bearing. `naptan_dataset.csv` is a subset filtered to Edinburgh.
  Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
- **[postcodes.io](https://postcodes.io)**: postcode geocoding. Great Britain postcode data is used under the OS OpenData licence.
  Contains Ordnance Survey data © Crown copyright and database right 2025.
  Contains Royal Mail data © Royal Mail copyright and database right 2025.
  Contains National Statistics data © Crown copyright and database right 2025.
  Contains NRS data © Crown copyright and database right 2025.

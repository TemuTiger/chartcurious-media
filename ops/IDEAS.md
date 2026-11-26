# Idea backlog (pick from the top; mark used ones with the post ID)
| # | Hook | Likely data |
|---|---|---|
| 1 | ✅ USED s005 — Which countries get the most power from wind? | owid/energy-data wind_share_elec |
| 2 | ✅ USED s007 (share vs output since 2007 peak) — Coal's share of world electricity: how far has it fallen? | owid/energy-data coal_share_elec, World |
| 3 | ✅ USED s003 (per-person CO2) — China emits the most CO2 in total, but who emits most per person? (top 10 large countries) | owid/co2-data |
| 4 | ✅ USED s009 (generation per person, 2024) — Which country uses the most electricity per person? | owid/energy-data per_capita_electricity |
| 5 | Nuclear: which countries rely on it most? | owid/energy-data nuclear_share_elec |
| 6 | Australia vs the world: how clean is our electricity? | owid/energy-data carbon_intensity_elec |
| 7 | How much of the UK's power came from coal in 2012 vs now? | owid/energy-data |
| 8 | Which countries have emitted the most CO2 ever (cumulative)? | owid/co2-data cumulative_co2 |
| 9 | Hydropower: the countries that run almost entirely on water | owid/energy-data hydro_share_elec |
| 10 | Oil: who uses the most per person? | owid/energy-data oil_energy_per_capita |
| 11 | Gas vs coal in the US electricity mix, 2005 vs latest | owid/energy-data |
| 12 | Who emits more: aviation or shipping? (only if a reliable dataset is reachable) | check before use |
| 13 | Population: which countries will add the most people by 2050? | datasets/population or UN via OWID if reachable |
| 14 | The world's most populous countries, 1950 vs today | datasets/population |
| 15 | ✅ USED s008 (2023, Australia vs 10 biggest economies) — GDP per person: Australia vs the biggest economies | datasets/gdp + population |
| 16 | Which country gets most of its energy (not just electricity) from renewables? | owid/energy-data renewables_share_energy |
| 17 | Germany's electricity mix: 2000 vs latest | owid/energy-data |
| 18 | Which countries have cut CO2 the most since 1990? | owid/co2-data |
| 19 | Low-carbon electricity leaders (nuclear + renewables) | owid/energy-data low_carbon_share_elec |
| 20 | Solar in Australia: share by year | owid/energy-data |
| 21 | India's electricity: how much is still coal? | owid/energy-data |
| 22 | Emissions per dollar of GDP: who is most efficient? | owid/co2-data co2_per_gdp |
| 23 | Methane: top emitters | owid/co2-data methane if present |
| 24 | Which countries import the most emissions (consumption vs production CO2)? | owid/co2-data consumption_co2 |
| 25 | Electricity demand growth: fastest-growing big countries | owid/energy-data |
| 26 | Quiz format: guess which country is #1 (reveal last) | any of the above |
| 27 | Then vs now: 1990 vs latest for a surprising metric | any |
| 28 | "Your country" series: top 10 by share of wind+solar | owid/energy-data |
| 29 | Biggest oil producers per person | owid/energy-data oil_prod_per_capita |
| 30 | Which country's electricity is dirtiest per kWh? | owid/energy-data carbon_intensity_elec |

## Broadened backlog (added 25 Nov after advice review; D009 covers money, sport, history and everyday life, not only energy)
Rule: alternate energy/climate with a non-energy topic. Rank = expected audience pull (broad relatability × surprise). Check the data is reachable and reputable before use; skip if not.
| Rank | Hook | Likely data | Format idea |
|---|---|---|---|
| 1 | ⏭ SKIPPED 26 Nov: only 2019 data reachable on GitHub raw (owid-datasets); retry if a current UN WPP file is reachable — Which countries have the longest life expectancy, and where does Australia rank? | OWID life expectancy (UN WPP) | single chart |
| 2 | ✅ USED s004 (as 1960-2025 people added; World Bank data starts 1960) — The world's population in 1950 vs today: who grew the most? | datasets/population | then vs now |
| 3 | ✅ USED s006 (as US$ price, July 2026; wage data not in the repo) — How long would you work to buy a Big Mac in different countries? | The Economist big-mac-index GitHub | quiz, reveal last |
| 4 | Which countries have won the most Olympic gold medals per person? | Olympic medal tables + population (check source) | single chart |
| 5 | How many hours a year do people work in different countries? | OWID annual working hours (Penn World Table) | single chart |
| 6 | The countries where people are getting taller fastest | OWID human height (NCD-RisC) | then vs now |
| 7 | Which countries have the most tourists per resident? | OWID / UN Tourism (check) | single chart |
| 8 | How much has a person's income grown since 1990? Australia vs others | datasets/gdp + population | then vs now |
| 9 | Fertility rate: how many countries are now below 2 children per woman? | OWID fertility (UN WPP) | counter + chart |
| 10 | Which countries have the most people over 65? | OWID / UN WPP | single chart |
| 11 | Internet use: how fast did the world get online? | OWID share using the internet (ITU) | line race |
| 12 | Which countries eat the most meat per person? | OWID meat supply (FAO) | single chart |
| 13 | Child mortality 1950 vs today | OWID child mortality (UN IGME) | then vs now |
| 14 | Literacy: the countries that changed fastest | OWID literacy | then vs now |
| 15 | 3-in-1 (35–60s, E004): "Three charts that show how much the world changed since 1990" | combine above | long format |

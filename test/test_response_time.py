from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from timeit import default_timer
from unittest import TestCase

import requests

address = """
2200 S Fort Apache Rd
2150 W Alameda Rd
200 W Sahara Ave
3151 Soaring Gulls Dr
2700 Las Vegas Blvd S
2725 S Nellis Blvd
2300 E Silverado Ranch Blvd
3935 E Rough Rider Rd
231 W Horizon Ridge Pkwy
10550 W Alexander Rd
1701 E Colter St
1405 Vegas Valley Dr
2120 Ramrod Ave
2750 S Durango Dr
3318 N Decatur Blvd
2402 E 5th St
353 E Bonneville Ave
2725 E Mine Creek Rd
3726 Las Vegas Blvd S
3722 Las Vegas Blvd S
1100 N Priest Dr
2305 W Horizon Ridge Pkwy
2451 N Rainbow Blvd
2900 Sunridge Heights Pkwy
222 Karen Ave
322 Karen Ave
11640 N Tatum Blvd
1825 W Ray Rd
251 S Green Valley Pkwy
10001 Peace Way
1881 W Alexander Rd
2700 N Rainbow Blvd
150 Las Vegas Blvd N
1575 W Warm Springs Rd
3145 E Flamingo Rd
1050 E Cactus Ave
2251 Wigwam Pkwy
3400 Cabana Dr
14575 W Mountain View Blvd
2050 W Warm Springs Rd
14250 W Wigwam Blvd
10330 W Thunderbird Blvd
10245 S Maryland Pkwy
3134 E McKellips Rd
3150 Soft Breezes Dr
11275 N 99th Ave
2555 Hampton Rd
1961 N Hartford St
2777 Paradise Rd
3236 E Chandler Blvd
2401 E Rio Salado Pkwy
2851 S Valley View Blvd
1455 E Katie Ave
235 E Ray Rd
3111 Bel Air Dr
13700 N Fountain Hills Blvd
1225 N 36th St
15221 N Clubgate Dr
1830 N Buffalo Dr
2025 E Campbell Ave
2455 W Serene Ave
12221 W Bell Rd
1645 W Baseline Rd
3125 N Buffalo Dr
18416 N Cave Creek Rd
286 W Palomino Dr
3810 N Maryvale Pkwy
12222 N Paradise Village Pkwy W
3302 N 7th St
2300 E Magma Rd Spc A
1920 E Bell Rd
200 E Southern Ave
15240 N 142nd Ave
20802 N Grayhawk Dr
2747 Paradise Rd
10809 Garden Mist Dr
3825 E Camelback Rd
170 E Guadalupe Rd
2877 Paradise Rd
30 Strada Di Villaggio
1432 W Emerald Ave
1851 Hillpointe Rd
2615 W Gary Ave
2606 S Durango Dr
2201 Ramsgate Dr
2857 Paradise Rd
3823 S Maryland Pkwy
2024 S Baldwin
2405 W Serene Ave
200 Hoover Ave
30 E Brown Rd
14200 W Village Pkwy
29 Montelago Blvd
125 S 56th St
280 S Evergreen Rd
207 W Clarendon Ave
3434 E Baseline Rd
10115 E Mountain View Rd
12123 W Bell Rd
2801 N Rainbow Blvd
2134 E Broadway Rd
2291 W Horizon Ridge Pkwy
1405 S Nellis Blvd
1340 N Recker Rd
1500 W Rio Salado Pkwy
3131 E Legacy Dr
1 E Lexington Ave
1525 Spiced Wine Ave
220 N 22nd Pl
3131 W Cochise Dr
2325 Windmill Pkwy
101 Luna Way
1055 N Recker Rd
1265 S Aaron
205 E Harmon Ave
3510 E Hampton Ave
210 E Flamingo Rd
14002 N 49th Ave
220 E Flamingo Rd
230 E Flamingo Rd
260 E Flamingo Rd
3450 Erva St
270 E Flamingo Rd
3425 E Russell Rd
17606 N 17th Pl
1600 N Saba St
1235 N Sunnyvale
16825 N 14th St
1111 E University Dr
1800 Edmond St
3135 S Mojave Rd
11280 Granite Ridge Dr
2524 S El Paradiso
3800 S Cantabria Cir
1550 N Stapley Dr
18202 N Cave Creek Rd
1970 N Hartford St
2250 E Deer Valley Rd
1830 N Pecos Rd
2323 N Central Ave
2925 Wigwam Pkwy
2201 N Comanche Dr
295 N Rural Rd
1222 E Baseline Rd
2600 E Springfield Pl
15550 N Frank Lloyd Wright Blvd
3930 Swenson St
1015 S Val Vista Dr
1601 N Saba St
3119 W Cochise Dr
38 E Serene Ave
2625 E Indian School Rd
2019 W Lemon Tree Pl
2875 W Highland St
18250 N Cave Creek Rd
1101 S Sycamore
16620 S 48th St
1741 S Clearview Ave
1211 N Miller Rd
1750 W Union Hills Dr
2080 Karen Ave
16 W Encanto Blvd
2050 Los Feliz St
17 W Vernon Ave
2975 Bluegrass Ln
2727 N Price Rd
1411 E Orangewood Ave
10828 N Biltmore Dr
16657 E Gunsight Dr
21 E 6th St
15215 N Kierland Blvd
18611 N 22nd St
1716 W Cortez St
2831 E Southern Ave
255 N Kyrene Rd
32 E Serene Ave
16402 N 31st St
33550 N Dove Lakes Dr
1333 E Morten Ave
17150 N 23rd St
1111 N 64th St
18239 N 40th St
356 E Desert Inn Rd
2477 W Market Pl
17365 N Cave Creek Rd
15402 N 28th St Ci20
26 E Serene Ave
3327 Erva St
350 S Durango Dr
360 E Desert Inn Rd
1717 E Morten Ave
1515 E Reno Ave
1702 W Tuckey Ln
3845 E Greenway Rd
22125 N 29th Ave
10757 N 74th St
16410 S 12th St
10401 N 52nd St
1300 S Arlington St
2565 S Signal Butte Rd
3375 E Tompkins Ave
2995 E Sunset Rd
1310 S Pima
1017 E Maryland Ave
13600 N Fountain Hills Blvd
14450 N Thompson Peak Pkwy
2220 W Dora St
10015 E Mountain View Rd
10017 E Mountain View Rd
123 N Washington St
2155 N Grace Blvd
1505 N Center St
3445 N 36th St
1125 E Broadway Rd
1215 E Lemon St
15020 N 40th St
1950 N Center St
2233 E Highland Ave
1850 S Westwood
2035 E Warm Springs Rd
3455 Erva St
2311 E Hartford Ave
2910 W Marconi Ave
15 E Agate Ave
208 W Portland St
2626 E Arizona Biltmore Cir
31 E Agate Ave
35 E Agate Ave
3921 W Ivanhoe St
27 E Agate Ave
17 E Ruth Ave
3930 W Monterey St
20 E Serene Ave
2312 W Lindner Ave
124 N California St
2000 N 36th St
1352 E Highland Ave
2775 W Pebble Rd
385 W Pierson St
1326 N Central Ave
19 E Agate Ave
23 E Agate Ave
2737 E Arizona Biltmore Cir
39 E Agate Ave
10807 W Northern Ave
1130 N 2nd St
11441 Allerton Park Dr
20 S Buena Vista Ave
2831 Geary Pl
2866 Loveland Dr
1932 N Mesa Dr
2256 W Lindner Ave
3030 N Hayden Rd
3318 N 18th Ave
1229 N Alma School Rd
16021 N 30th St
1381 E University Ave
14849 N Kings Way
15430 N 25th St
16015 N 30th St
1406 W Emerald Ave
17223 N Cave Creek Rd
3230 E Pinchot Ave
125 N Sunvalley Blvd
151 E Broadway Rd
100 W Portland St
2150 W Missouri Ave
15801 N 29th St
3567 Arville St
1065 W 1st St
1102 W Glendale Ave
13227 N Mimosa Dr
3030 N 38th St
1908 Villa Palms Ct
12050 N Panorama Dr
2201 E Pinchot Ave
1624 E Campbell Ave
1630 E Georgia Ave
100 W Maryland Ave
1336 E Mountain View Rd
1530 E Maryland Ave
16336 E Palisades Blvd
2961 Country Manor Ln
37222 N Tom Darlington Dr
16734 E Gunsight Dr
11251 Hidden Peak Ave
11256 Rainbow Peak Ave
1440 Vegas Valley Dr
16528 E Gunsight Dr
1816 W Tuckey Ln
1866 Via Delle Arti
211 Mission Laguna Ln
2111 Sealion Dr
2121 Blue Breeze Dr
220 Mission Catalina Ln
2970 N Oregon St
353 Amber Pine St
1301 W 4th St
3110 N 40th St
10552 Pine Pointe Ave
10553 Pine Pointe Ave
16540 E Gunsight Dr
16807 E Gunsight Dr
1908 High Valley Ct
2019 Rancho Lake Dr
2101 Hussium Hills St
2141 Hussium Hills St
2171 Hussium Hills St
300 Pine Haven St
3750 Shirebrook Dr
3769 Carlyle Dr
305 S Wilson St
325 E Palm Ln
1008 Domnus Ln
1012 Domnus Ln
1077 W 1st St
14814 N 24th Dr
1900 Desert Falls Ct
1901 High Valley Ct
301 Pine Haven St
3591 Arville St
13804 N Saguaro Blvd
1414 E Grovers Ave
1900 Rio Canyon Ct
3119 N 38th St
323 S Roosevelt St
10600 Amber Ridge Dr
10620 Amber Ridge Dr
10700 Amber Ridge Dr
10711 Pappas Ln
11835 Portina Dr
11850 Tevare Ln
11855 Portina Dr
2019 E Campbell Ave
206 E Lawrence Blvd
2140 Pinetop Ln
2180 Pinetop Ln
3676 Renovah St
3677 Renovah St
1419 S Kenneth Pl
17032 N 16th Dr
2000 Jasper Bluff St
2001 Quarry Ridge St
2001 Quartz Cliff St
2053 Quarry Ridge St
2101 Quarry Ridge St
2152 Turquoise Ridge St
2153 Quartz Cliff St
3350 Cactus Shadow St
3420 Mercury St
3451 Desert Cliff St
3500 Mercury St
3561 Arville St
3573 Arville St
10021 Crimson Palisades Pl
10150 Cedar Key Ave
10155 Cedar Key Ave
10213 King Henry Ave
10217 King Henry Ave
10233 King Henry Ave
10245 King Henry Ave
10270 Gilmore Canyon Ct
10290 Gilmore Canyon Ct
10640 Calico Mountain Ave
10650 Calico Mountain Ave
12800 N 113th Ave
1311 Red Gable Ln
1400 Seward St
1401 Linnbaker Ln
1410 Red Crest Ln
1460 Di Blasi Dr
14951 E Desert Willow Dr
1505 Blackcombe St
1509 Blackcombe St
1521 Ruby Cliffs Ln
1531 Ruby Cliffs Ln
1617 Queen Victoria St
1701 King James St
1704 Queen Victoria St
1725 Queen Victoria St
1806 N Decatur Blvd
1810 N Decatur Blvd
1820 N Decatur Blvd
1826 N Decatur Blvd
1828 N Decatur Blvd
1836 N Decatur Blvd
1844 N Decatur Blvd
1846 N Decatur Blvd
1850 N Decatur Blvd
1854 N Decatur Blvd
1856 N Decatur Blvd
1860 N Decatur Blvd
1925 Hodgenville St
20420 N 6th Dr
2113 Echo Bay St
2120 Calville St
2961 Juniper Hills Blvd
2963 Juniper Hills Blvd
2965 Juniper Hills Blvd
2977 Juniper Hills Blvd
2979 Juniper Hills Blvd
2982 Juniper Hills Blvd
2983 Juniper Hills Blvd
2984 Juniper Hills Blvd
2986 Juniper Hills Blvd
3046 Tarpon Dr
3050 Tarpon Dr
3055 Casey Dr
3058 Casey Dr
3058 Tarpon Dr
3064 Casey Dr
3065 Casey Dr
3066 Tarpon Dr
3079 Key Largo Dr
3083 Key Largo Dr
3111 Key Largo Dr
3131 Key Largo Dr
3155 Casey Dr
316 W Tonopah Dr
3174 Tarpon Dr
3364 Indian Shadow St
3395 Cactus Shadow St
3450 Cactus Shadow St
3475 Cactus Shadow St
3480 Cactus Shadow St
3500 Winterhaven St
3504 Desert Cliff St
3511 Desert Cliff St
3512 Winterhaven St
3515 Cactus Shadow St
3541 Desert Cliff St
3544 Desert Cliff St
3571 Desert Cliff St
3574 Desert Cliff St
3604 Di Salvo Dr
3605 Melonies Dr
3608 Melonies Dr
3812 Ormond Beach St
3815 Juno Beach St
3830 Wiggins Bay St
3845 Wiggins Bay St
10201 Deerfield Beach Ave
10215 N 8th Ave
10601 Pedal Point Pl
1201 E Rose Ln
1214 W 5th St
1456 S Boulder St
3537 Mercury St
3840 Belle Glade St
1004 E Osborn Rd
10180 Delray Beach Ave
10190 Delray Beach Ave
10191 Deerfield Beach Ave
10230 Deerfield Beach Ave
10230 Delray Beach Ave
11346 Bedford Commons Dr
1164 S Boulder St
1400 San Juan Hills Dr
1405 San Juan Hills Dr
1420 Jamielinn Ln
1508 Blackcombe St
1508 Truett St
1515 E Sahuaro Dr
1551 Linnbaker Ln
1560 Plaza Centre Dr
1576 E Orchid Ct
1608 Hills Of Red Dr
1608 Queen Victoria St
1609 Hills Of Red Dr
1621 Sandecker Ct
1701 Sandecker Ct
1713 Sky Of Red Dr
18621 N 34th Ave
1920 Hodgenville St
1921 Summerville St
2152 Quartz Cliff St
2200 Comet Ave
22026 N 103rd Ln
2517 Danborough Ct
2524 Charleville Ave
2603 S Durango Dr
2641 S Durango Dr
3324 W McRae Way
3401 W Morrow Dr
10720 Amber Ridge Dr
11318 McKinney Falls St
11410 Belmont Lake Dr
11500 Belmont Lake Dr
1371 S Boulder St
16729 E Westby Dr
3408 Mercury St
1029 E Roosevelt St
1100 Willow Tree Dr
1108 Observation Dr
111 Bass Dr
1128 Willow Tree Dr
1133 Willow Tree Dr
11338 Belmont Lake Dr
11417 Ogden Mills Dr
11488 Belmont Lake Dr
11512 Belmont Lake Dr
1205 N Buffalo Dr
1209 N Buffalo Dr
1212 Bass Dr
12217 N 21st Ave
12245 N 21st Ave
12641 N Mimosa Dr
1309 Markwood Cir
1317 Driscoll Dr
1320 Pinto Rock Ln
1404 Santa Anita Dr
1417 Hialeah Dr
1452 Dorothy Ave
1460 Hialeah Dr
14621 N 37th Pl
14632 N 37th St
1480 Tamareno Cir
1481 Living Desert Dr
14960 E Desert Willow Dr
1497 Dorothy Ave
1551 Plaza Centre Dr
1600 Burningwood Ln
1616 Burningwood Ln
16741 E Westby Dr
17031 E Calle Del Oro
18045 N 20th Dr
18225 N 31st Ave
2110 Bavington Dr
2117 Chertsey Dr
2125 Sun Ave
2143 E 10th St
220 Shadybrook Ln
2201 Sun Ave
2350 Canfield Dr
2373 Cardiff Ln
241 Misty Isle Ln
2501 Sierra Bello Ave
2520 Sierra Bello Ave
2521 Perryville Ave
2529 Charleville Ave
2696 N 43rd Ave
2720 Otter Creek Ct
2825 E Waltann Ln
2929 Siki Ct
3077 Pinehurst Dr
3173 Pinehurst Dr
320 Brookside Ln
3211 Sunfish Dr
3231 Jericho St
3274 Andrea St
3482 Lorilou Ln
3505 Rio Robles Dr
3600 Galatea St
3605 Arginis St
3708 Scuba Cir
3955 Palm Beach St
3961 Rebecca Raiter Ave
10084 Sunset Palisades Way
10132 Sunset Palisades Way
10145 Malibu Creek Ct
10231 Delray Beach Ave
10411 N 9th St
1066 Sheer Paradise Ln
1070 Cryer Ct
1081 Pleasure Ln
1089 Elation Ln
1099 Sheer Paradise Ln
1109 Pleasure Ln
1114 Luna Eclipse Ln
11227 Cactus Tower Ave
1125 Tuscan Sky Ln
11278 Kraft Mountain Ave
11302 Kraft Mountain Ave
1143 Grass Pond Pl
1149 Red Margin Ct
11620 N 31st Dr
1173 Red Margin Ct
1305 Allegheny Moon Ter
1335 Grass Creek Ave
1350 Crystal Hill Ln
1351 Grass Creek Ave
1355 Grass Creek Ave
1358 Crystal Hill Ln
1362 Grass Creek Ave
139 S 108th Dr
14046 N 39th Ln
14219 N Brunswick Dr
15015 N 20th Pl
15035 N 28th Dr
15345 N Scottsdale Rd
16036 N 70th Dr
1944 Summer Palm Pl
2092 Benelli Ferry Ct
2311 Koho Dr
2348 Yellowstone Creek Dr
2627 S Lamb Blvd
2738 S Voyager Dr
2748 S Cavalier Dr
3136 N 37th St
3208 Regal Swan Pl
3209 Orange Orchid Pl
3216 Regal Swan Pl
3312 Speckle Summer Pl
335 Clarence House Ave
3416 President Pride Pl
3425 Conan St
36 Hudson Canyon St
3913 Pepper Thorn Ave
3932 Pepper Thorn Ave
3933 Pepper Thorn Ave
3936 Smokey Fog Ave
100 W Palm Ln
1020 W Georgia Ave
10311 N 96th Ave
1053 E Weldon Ave
10636 N 114th Ave
10842 N 41st Ave
1118 W Roosevelt St
11222 N 69th Dr
1125 E Devonshire Ave
1133 N Nielson St
1145 W 12th Pl
11613 N 76th Ln
11803 N 96th Pl
1309 W 7th Pl
13212 N 3rd St
13302 N 26th Ave
1339 E Marlin Dr
13418 S 47th Pl
13808 N 33rd St
13839 N 19th St
14102 N 127th Ave
1422 W McLellan Blvd
14228 N 45th Ave
1469 Rothwell Ct
14825 N 35th St
15131 N Ivory Dr
15207 N 37th Way
1524 W 5th Pl
153 N Ocotillo Dr
15427 N Jerry St
1581 W Del Rio St
15830 S 15th Pl
15838 N 6th Dr
15895 N 74th Dr
1602 E Ocotillo Rd
1602 W McDowell Rd
16030 S 10th St
1615 W Bluefield Ave
16429 E Ashbrook Dr
1700 S College Ave
17425 N 16th Pl
1767 E Redfield Rd
17814 N 34th Pl
18433 N 45th St
1875 W Aspen Ave
19210 N 14th St
19230 N 4th Pl
1940 N 77th Gln
2019 Turney Ave
20227 N 21st Dr
20626 N 29th Dr
2109 N 109th Ave
21906 N 36th Way
2233 W Beverly Ln
2241 E Heatherbrae Dr
2241 E Isabella Ave
2242 N 29th St
2326 E Pinchot Ave
2401 N 92nd Ln
2444 E Danbury Rd
2519 N 29th St
2530 N 3rd St
2531 N 73rd Dr
2548 W Georgia Ave
2617 N 71st Pl
2622 E Fawn Dr
2628 E Orange St
26819 N 84th Ln
2801 N 71st Pl
2821 Turney Ave
3007 N 25th Dr
3022 N 34th Pl
3031 N 69th Pl
307 E Mariposa St
3141 E Cypress St
321 W Medlock Dr
3313 S 80th Dr
3420 W Laurel Ln
3611 E Sunnyside Dr
3614 W Lawrence Ln
396 Hillhead Ct
1 Spur Cross Cir
10 Golf View Dr
100 Almarte Dr
1000 W 5th St
10003 Elendil St
10004 Pinnacle View Pl
10006 Tittleton Ave
10007 W Montecito Ave
1001 W Danbury Rd
1001 W Indian School Rd
10011 Sable Point St
10012 La Paca Ave
10016 N 66th Dr
1002 W Greenway Dr
10025 Artistic Walk Ave
10025 Mystic Dance St
10027 E Obispo Ave
10032 W Riviera Dr
10034 Sable Point St
10037 Capistrello Ave
10037 Portula Valley St
1004 Blue Lantern Dr
10041 E Impala Ave
10041 Tenerife St
10043 E Sheena Dr
10043 Fragile Fields St
10049 Twilight Canyon Ct
1005 Appaloosa Hills Ave
1005 Secret Garden St
10052 Oyster Pearl St
10054 Delicate Dew St
1006 Grand Cerritos Ave
10060 E San Bernardo Dr
10063 Cambridge Blue Ave
10064 San Gervasio Ave
10067 S Riley St
1007 Golden Ridge Ct
10074 Hawthorne Grove St
10076 Golden Bluff Ave
1008 Calvia St
1008 Miradero Ln
10081 E Turquoise Ave
10084 Flagstaff Butte Ave
1009 Dusty Creek St
1009 Paradise View St
1009 Sir James Bridge Way
1009 Snow Bunting Ct
10091 Walsh River Ave
10093 Whitney Falls Ct
10095 San Gervasio Ave
1010 S Bogle Ct
1011 Klamath River Ave
10111 E Tierra Buena Ln
10116 Marvel Cove St
1012 Brinkman St
1012 Grey Hollow Ave
1012 S Wagon Wheel Dr
10121 Cardinal View Pl
10122 E Illini St
10124 Eden Falls Ln
10125 Middle Ridge Dr
10125 Quaint Tree St
10128 Marvel Cove St
1013 Puerta Del Sol Dr
1013 Shades End Ave
1013 W Cornell Dr
1013 W Parkway Blvd
10137 E Conieson Rd
10139 E Knowles Ave
1014 Brookside Ct
1014 Date St
1014 Emerald Stone Ave
1014 Paradise View St
1014 W Redondo Dr
1015 Ridgegate St
10153 Maidens Wreath Ct
10159 Deep Glen St
1017 Brinkman St
1017 Cliffbrook Hedge Ave
10172 Arlington Abby St
10175 Palazzo Marcelli Ct
10185 Lucca Bluff St
10185 Maltese Cross Ct
10190 Moth Orchid Ct
10190 N 106th St
10191 Rising Tree St
102 Beaver Ridge Ave
1020 Aspen Hill Cir
1020 Miradero Ln
1020 Pagosa Way
10206 N Demaret Dr
10207 Ghost Gum St
10217 San Giano Pl
10218 W Veliana Way
1022 W Helena Dr
10220 Glen Ora Ave
10221 W Wier Ave
10224 Black Friar Ct
10225 Climbing Lily St
10229 Yarmouth Sea Ct
1023 New Creek Ave
10231 Songsparrow Ct
10238 E Blanche Dr
10238 Early Morning Ave
1024 S Cheshire Ln
10252 Moth Orchid Ct
10255 Danskin Dr
10256 Copparo Pl
10258 E Spring Creek Rd
1026 E Pierce St
10272 Ghost Gum St
10273 Headrick Dr
10276 Romantico Dr
1028 Logan Patrick Dr
1028 Olive Mill Ln
1028 W 22nd Ave
10280 Splendor Ridge Ave
1029 E Jasper Dr
10293 Jersey Shore Ave
10294 Spider Rock Ave
103 Short Ruff Way
103 Willow Dove Ave
10304 New Frontier Ln
10305 Saugus Dr
10305 W Windsor Ave
10307 E Billings St
1031 E Sunset Rd
10310 E Le Marche Dr
10311 Mystic Pine Rd
1032 Baronet Dr
10321 W Monterosa Ave
10322 W Cinnebar Ave
10326 E Le Marche Dr
10326 W Missouri Ave
10327 Juniper Creek Ln
10330 Blue Claws Ln
10336 Birch Bluff Ln
10337 Profeta Ct
10340 Falls Church Ave
10342 Pescado Ln
10344 E Sharon Dr
10348 Melon Cactus St
10349 Adams Chase St
10356 Pink Cloud Ct
10357 Talking Tree Ave
10359 Wood Plank Ln
10363 Hardy Falls St
10366 Denman St
1037 Valley Light Ave
1038 Havenworth Ave
1038 S 167th Dr
10384 Lady Angela St
10385 W Yukon Dr
10387 Pima Crossing Ave
10392 Mystic Pine Rd
10396 Walking View Ct
10398 Catclaw Ct
104 Ash St
10401 S 44th Pl
10404 Garland Grove Way
10408 W Echo Ln
10409 Bent Willow Ave
10409 N 58th Ln
10409 Orkiney Dr
1041 Augusta Wood Ct
1041 W Desert Hills Dr
10413 E Natal Ave
10413 Linfield Pl
10418 Gabaldon St
10421 Horseback Ridge Ave
10421 Niagara Falls Ln
10421 Shadowland Ave
1043 E Maryland Ave
10430 W Oregon Ave
10433 Concetta Ave
10441 Concetta Ave
10442 Masons Creek St
10448 Perfect Parsley St
10451 Processor Ct
10454 E Texas Sage Ln
10458 N 9th St
10460 Bay Ginger Ln
10465 Canyon Cliff Ct
10468 Concetta Ave
10469 Abisso Dr
10469 Howling Coyote Ave
10471 Sweet Juliet St
10476 E Hillery Dr
1048 Brinkman St
1048 Sweet Elderberry Ct
10480 Howling Coyote Ave
10482 Gabaldon St
10487 Beckaville Ave
10487 Perfect Peace Ln
10490 Lilac Tree Ave
105 Snow Dome Ave
1050 S Wanda Dr
10500 Abisso Dr
10501 Back Plains Dr
10503 N 76th Dr
10508 White Heath Ct
10511 E Corbin Ave
10512 Galleon Peak Ln
10513 Beachwalk Pl
1052 Brinkman St
10522 Gold Shadow Ave
10522 Mojave Ridge Ct
10524 W Preston Ln
10527 Snow Lake St
10530 W Bayside Rd
10531 Lilac Tree Ave
10532 Allthorn Ave
10542 E Terra Dr
10544 Allthorn Ave
10545 E Mission Ln
10546 Pueblo Springs St
10550 E Boulder Dr
10553 Laurelwood Lake Ave
10555 Acacia Park Pl
10558 Cliff Lake St
1056 Country Skies Ave
10560 Midnight Gleam Ave
10572 San Sicily St
1058 Bellevue Peak St
10584 Bella Camrosa Dr
10584 Moultrie Ave
10589 Bardilino St
1059 W Sandy Banks
10590 W Salter Dr
10596 Bardilino St
10599 W Desert Star Ln
106 Parker Ranch Dr
106 Tall Ruff Dr
10601 Esk Dr
10607 E Autumn Sage Dr
1061 Aspen Cliff Dr
10613 Austin Bluffs Ave
10613 Golden Aspen Ct
10616 Primrose Arbor Ave
10619 Auburn Springs Ave
10621 Brianhurst Ave
10622 Piombino St
10624 E Portobello Ave
10625 Wildhurst St
10626 Corte Sierra St
10626 W Zak Rd
10633 Double Spring Ct
10646 E Betony Dr
10648 Yarmouth Key Ct
10652 Cosenza Ln
10654 El Camino Rd
1068 Silver Creek Ave
10680 Foggy Glen Ave
10686 Allegrini Dr
107 W Victory Rd
10705 E Acoma Dr
10708 Cedar Creek Ave
10709 Cedar Creek Ave
10711 Iona Island Ave
10718 Azure Ocean Ave
1072 Wainwright Ct
10724 Paradise Point Dr
10728 Sleepy Mist Ct
10734 Vemoa Dr
10741 Muscari Way
10745 Rococo Ct
10747 Holmfield St
10748 W Bronco Trl
10749 Refectory Ave
10749 W Ruth Ave
1076 Spotted Bull Ct
10762 Flame Vine Ct
10768 Tottenham Ave
10771 W 2nd St
1078 E Silktassel Trl
10788 Maltese Falcon Ave
10792 N 124th Pl
10798 W Del Rio Ln
108 Beech St
108 Blackberry Ln
108 N Cholla St
108 N Minnesota St
10800 Maltese Falcon Ave
10808 Date Creek Ave
10808 N 64th Ln
10811 Ackers Dr
10813 E Verbina Ln
10814 Drake Ridge Ave
10816 Ackers Dr
10817 W Windsor Ave
10819 Bayview House Ave
1082 W Windhaven Ave
10820 Woods Hole Bay St
10822 W El Dorado Dr
10825 W Madison St
10829 W Amber Trl
1083 Via Saint Lucia Pl
10833 Elfstrom Ave
10841 W Canterbury Dr
10841 W Louise Dr
10843 E Mercer Ln
10851 W Avenida Del Rey
10853 Dornoch Castle St
10862 Avenzano St
10876 Fishers Island St
10880 Woods Hole Bay St
10884 Royal Highlands St
10885 Fintry Hills St
1089 Jesse Harbor Ave
10891 Carberry Hill St
10899 Fishers Island St
109 Golf Course St
109 Strone St
10908 Calistoga Springs Ct
10912 Sutter Hills Ave
10914 W Lewis Ave
10916 W Elm St
10925 W Kaler Dr
10933 E Wier Ave
10937 Sutter Hills Ave
10941 Toscano Gardens St
10944 Mount Stellar St
10963 Carberry Hill St
10966 Santorini Dr
10968 Tranquil Waters Ct
10977 African Sunset St
1098 Broadmoor Ave
10993 Ladyburn Ct
10994 Tionesta Ct
11 Hazeltine Ln
11 N Soho Pl
11 New Mexico Way
110 E La Jolla Dr
110 W Maryland Ave
11001 W Frier Dr
11005 W Alabama Ave
11006 W Woodland Ave
11009 Dornoch Castle St
11013 W Mariposa Dr
11021 Sonoma Creek Ct
11022 Vasari Ct
11024 Meadow Leaf Ave
11025 Okeefe Ct
11032 Rackhurst Ave
11040 N 58th Dr
11040 W Hayward Ave
11041 N 17th Dr
11043 Parete Ct
11046 E Serafina Ave
11052 E Jasmine Dr
11061 Zarod Rd
11063 Alora St
11067 E Butherus Dr
11072 Piedmont Valley Ave
1108 Cashman Dr
11082 W Ruth Ave
1109 E Gail Dr
111 Broken Putter Way
11109 Whooping Crane Ln
11110 W Montecito Cir
1112 N Wade Dr
1112 W Nopal Pl
11120 W Ashbrook Pl
11121 Rossi Ave
11126 W Wilshire Dr
1113 Copper Grass St
11133 Sundad St
11135 E Greenway Rd
1114 Majestic Canyon St
1114 Oak Island Dr
11140 Rose Reflet Pl
11146 E Running Deer Trl
11155 Grants Landing Ct
1116 W Dawn Dr
11164 Abbeyfield Rose Dr
11164 Salinas Pueblo St
11167 Ranch Valley St
11170 African Sunset St
11182 W Holly St
1119 N Owl Dr
112 Beech St
1120 Broken Hills Dr
1120 E Rome Blvd
1120 Little Rock Way
11201 Falesco Ave
11202 W Turney Ave
11208 Sandrone Ave
11216 Campanile St
11219 Sweetstem Ct
1122 Darmak Dr
11220 Rose Reflet Pl
11221 W Roanoke Ave
11222 W Coronado Rd
11229 Silent Hawk Ln
1123 Puffin Ct
11235 Villa Trentino Ct
11239 E Oberlin Way
11239 Playa Bonita Ave
11241 W Alice Ave
11246 Campanile St
11246 Ventura Grass Ct
11249 Newbury Hills Ave
1126 Bradley Bay Ave
1127 Echo Pass St
1128 E Jensen St
1128 Jesse Harbor Ave
11289 Victoria Medici St
1130 N Leoma Ln
11315 Colinward Ave
11318 Patores St
11324 N 81st Dr
11324 W Elm St
11327 E Beck Ln
11334 E Stearn Ave
1134 N April Cir
11343 E Quintana Ave
11349 W Loma Blanca Dr
1135 S 165th Dr
11357 Colinward Ave
1137 Bobby Basin Ave
1138 Cathedral Ridge St
11405 W Rio Vista Ln
11414 W Apache St
11415 N 45th Pl
1142 E San Tan Dr
11435 W Sheridan St
11458 W Foxfire Dr
11471 E Quartz Rock Rd
1148 Jesse Harbor Ave
11494 E Altadena Ave
11500 Valentino Ln
1151 W Hackamore St
11519 Via Princessa Ct
1152 Blue Magenta Ave
1152 Toro Hills Ct
11521 Evergreen Creek Ln
11522 W Bermuda Dr
11525 W Piccadilly Rd
11528 W Piccadilly Rd
11529 W Charter Oak Rd
1153 Country Shadows Way
11533 Cantina Terlano Pl
1154 Sierra Laurel Ct
11541 Bollinger Ln
11562 W La Reata Ave
11572 W Virginia Ave
11585 Stivali St
116 Boysenberry Ln
116 Palatial Pines Ave
1160 Nevada Sky St
11600 Evergreen Creek Ln
11609 W Charter Oak Rd
11611 Vesuvio Ct
11614 S Half Moon Dr
11615 Stivali St
1162 Paradise Safari Dr
11621 Cabo Del Verde Ave
11626 Sweet Nokia St
11631 Giles St
1164 Dana Maple Ct
11649 S 46th St
1165 Colgate Ln
11662 Elianto St
11663 Raveno Bianco Pl
11671 Primo St
1168 Paradise Home Rd
117 Breezy Shore Ave
117 E Valley View Dr
117 W 10th St
11705 Grotta Azzurra Ave
11709 Intervale Rd
1173 Paradise Mountain Trl
11741 Marina Grande Ct
11763 Longworth Rd
11767 W Banff Ln
1177 S Hazel St
11786 Pine Shadows St
11798 W Corrine Dr
118 Castle Course Ave
1180 Cottonwood Ranch Ct
1180 E Hacienda Ave
11802 W Poinsettia Dr
11816 Red Camellia Ave
1182 W Desert Basin Dr
11826 Bella Luna St
1183 King Arthur Ct
11830 Newport View St
11833 E Carol Ave
11835 Corenzio Ave
11835 N 151st Dr
11843 Cogoleto Ave
11880 E Appaloosa Pl
119 Colonial Springs Ct
1190 E Diamond Dr
11901 Fairfax Ridge St
11902 Giles St
11906 Port Labelle Dr
11913 Jersey Lilly St
11916 Alava Ave
11920 Amistoso Ln
11924 W Dahlia Dr
11929 Fairfax Ridge St
11932 May Weed Ct
11932 W Dahlia Dr
1194 Stormy Valley Rd
11945 Haven St
11959 W Berkeley Rd
11962 Camden Brook St
1198 Stormy Valley Rd
11993 W Almeria Rd
12 Copper Pine Ave
12 Greely Club Trl
120 Orland St
120 Painted Valley St
1200 Pyramid Dr
1201 E Escondido Dr
1201 E Weber Dr
1201 Palmares Ct
12011 W Windrose Dr
12018 N Rio Vista Dr
12021 W Avenida Del Rey
12033 Spice Tree St
12033 W Aster Dr
12037 Aragon Springs Ave
12044 W Desert Sun Ln
12049 Cielo Amber Ln
1205 Malibu Sands Ave
1205 N Mallard St
12050 W Carlota Ln
12057 W Rowel Rd
1208 W 6th St
1209 Hope Ranch Ln
1209 W Boston St
1209 Woodmore St
121 Crooked Putter Dr
121 W 10th St
1211 El Fuego Trl
12113 W Tether Trl
12118 W Hide Trl
1214 W Amelia Ave
12165 W Flanagan St
12168 W Yuma St
1217 Mews Ln
1219 E Lawrence Ln
1220 E Tremaine Ave
1220 Padre Serra Ln
12205 W Winslow Ave
1221 W Adams Ave
1223 W University Dr
12233 Argent Bay Ave
12247 La Prada Pl
12268 W Paso Trl
1227 E Tuckey Ln
12277 Old Muirfield St
12317 W Keim Dr
1232 E Broadmor Dr
1232 W Atlantic Dr
12326 E North Ln
12330 W Larkspur Rd
12334 W Rosewood Dr
12349 W Highland Ave
1235 Elizabeth Ave
1237 E Dust Devil Dr
1237 E Gemini Dr
12371 W Woodland Ave
124 La Padania Ave
1240 S Roger Way
12403 N Vista Grande Ct
12428 W San Miguel Ave
1243 W Sea Shell Dr
12446 W San Juan Ave
12461 W Granada Rd
1247 E Maryland Ave
12476 E Altadena Ave
12476 W Lindbergh Dr
125 E Solano Dr
125 Icy River Ave
125 Stockton Edge Ave
1250 E Hermosa Dr
12514 W Lisbon Ln
12525 W Bird Ln
1253 N Padre Kino Ln
1253 W Winchester Way
12531 W Campina Dr
12561 W Desert Flower Rd
1257 Morning Skyline Ct
1258 E Thompson Way
1259 E Iris Dr
1259 Panini Dr
126 Hickory St
126 Sunburst Creek Ave
1260 Golden Apple St
1260 W Straford Dr
1261 E Laurel Ave
1261 N Balboa Dr
12613 W Redondo Dr
12630 W Laurel Ln
12646 W Parkwood Dr
12649 W Charter Oak Rd
12649 W Shaw Butte Dr
12654 W Paradise Dr
1267 W Wilson Ave
12704 N 145th Way
12706 W Ash St
12710 W Willow Ave
1272 Panini Dr
12724 W Almeria Rd
1275 W Wilson Ave
1281 Sand Castle Ave
12815 W Voltaire Ave
1289 E Marcella Ln
129 Celia Pl
1290 N Salida Del Sol
12909 W Corrine Dr
12918 W Virginia Ave
1292 Raggedy Ann Ave
12921 N 127th Ln
12930 W Pershing St
12932 E Sahuaro Dr
12932 N Primrose St
12938 W Fleetwood Ln
12940 W Flower St
12949 W Scotts Dr
1295 Bayleaf Terrace Ave
13 Avenza Dr
13 W Zinnia Pl
130 Cloud Cover Ave
1300 Swanbrooke Dr
13005 W Evans Dr
1301 Franklin Ave
13018 W Lawrence Rd
1302 W 3rd St
13021 N 49th Pl
13025 W Windrose Dr
13028 N 70th St
1305 European Dr
13053 W Avalon Dr
1306 W El Alba Way
131 W Fellars Dr
1311 W Glendale Ave
1311 W Libby St
13110 W Cypress St
13112 W Rovey Ct
1312 W Libby St
13121 W Santa Ynez Ct
13122 W Wilshire Dr
1313 E Brill St
1314 E Thompson Way
1314 Francis Ave
1314 N 71st St
1316 E Carson Ave
1316 Lucia Dr
13165 N 80th Dr
1317 N 48th Pl
13173 E Primrose Ln
1318 Star Meadow Dr
13188 W Crocus Dr
13192 W Desert Ln
132 Tainted Berry Ave
1320 Rev Wilson Ave
13209 N 100th Ave
1321 Misty View Ct
1321 S Loomis
13210 N 126th Ave
13216 W Mauna Loa Ln
13224 W Stella Ln
13249 N 14th Dr
1326 Blue View Ct
1326 N 71st St
1327 Autumn Wind Way
1327 E Weatherby Way
1328 Kari Lee Ct
1328 Wheatland Way
133 Macoby Run St
1331 S 227th Ave
1333 E Grandview St
1333 Pacific Terrace Dr
1334 Stable Glen Dr
13340 N 149th Ave
13343 N 152nd Ave
134 E Ivy St
1341 W Pelican Ct
13419 N 102nd Pl
13420 W Tyler Trl
13424 W Desert Rock Dr
13435 N 33rd St
1344 E Don Carlos Ave
1344 W Roosevelt Ave
13449 W Rhine Ln
1347 E Briarwood Ter
1349 E Sahuaro Dr
135 Serenade Ct
1350 W Flintlock Way
1353 Fox Acres Dr
13549 W Berridge Ln
1355 Panini Dr
136 Villaggio St
1360 N Brentwood Pl
13602 N 82nd Ave
1364 Pattee Cir
13646 W Desert Flower Dr
13668 N 149th Dr
13714 W Marissa Dr
13719 W Keim Dr
138 Fratelli Ave
138 Montclair Dr
138 Newburg Ave
13817 N 149th Ln
13823 W Peck Dr
13839 W Peck Dr
1389 Dragon Rock Dr
1392 Baja Grande Ave
13940 N 132nd Ct
13960 W Country Gables Dr
1398 W Weatherby Way
14 New Mexico Way
1400 Bow Creek Ct
1400 Sweeney Ave
14017 N Burning Tree Pl
1403 W Michigan Ave
14032 E Cavedale Dr
1404 Pintail Point St
1404 Premier Ct
1408 Reebok Ter
1408 S 6th St
1409 Autumn Glen Cir
1409 Tumberry St
14097 W Dahlia Dr
14105 W Dahlia Dr
1411 E Fremont Dr
1412 S 16th St
14120 N 156th Ct
1413 W Coral Reef Dr
1414 W Hess Ave
1416 Andrew David Ave
1416 Kirby Dr
1416 S Jentilly Ln
1417 Blushing Bride St
1419 N 79th Ln
1419 W Sequoia Dr
142 Red Coral Dr
142 Rose Lake St
1420 W Missouri Ave
1421 Velvet Leaf Dr
14227 N 103rd Ave
1424 Iris Kelly Ave
1425 Muinos St
1425 Silk Tassel Dr
14256 N 2nd Ave
1426 E Brill St
14266 N Fountain Hills Blvd
1427 S Terrace Rd
14277 W Lexington Ave
14283 W Lexington Ave
1429 Bow Creek Ct
1429 Pathfinder Rd
1430 E Arrowhead Trl
1430 S Eucalyptus Pl
14300 N 160th Dr
1431 W Hess Ave
14310 W St Moritz Ln
1436 Still Creek Ave
144 W Ironwood Dr
1442 E Nighthawk Way
1442 S 77th Pl
14429 N 98th Pl
14431 W Clarendon Ave
14444 N 39th Way
14449 N 58th Ave
1446 Garden Cir
1446 Maryland Heights Ave
14466 W Verde Ln
14479 W Desert Flower Dr
1448 E Villa Maria Dr
1449 E Iris Dr
14495 N 135th Ln
1450 Verde Triandos Dr
14522 W Cameron Dr
14524 W Poinsettia Dr
14526 W Sierra St
1453 Hawaiian Hills Ave
14537 W Edgemont Ave
1454 E Tonto Dr
14555 N 132nd Ave
1463 W Swan Ct
14674 N Olympic Way
1471 E Dana Pl
14743 W Poinsettia Dr
14748 N 136th Ln
14756 W Poinsettia Dr
14818 N 38th St
14841 N 44th Pl
14850 N 60th Ave
1486 Arroyo Verde Dr
14860 N 174th Dr
14887 W Acapulco Ln
14892 W Laurel Ln
149 Voltaire Ave
14942 W Port Au Prince Ln
1499 Cilento Ct
15 Feather Sound Dr
15007 E Mustang Dr
15018 W Riviera Dr
15024 W Jackpot Way
15025 N 60th Dr
1503 E Todd Dr
15033 N 60th St
1504 Peyton Stewart Ct
1505 Waterton Dr
1505 Wintergreen Dr
15073 N 93rd Way
1509 W Flynn Ln
151 Castle Course Ave
15119 W Lilac St
1512 Remembrance Hill St
1516 Via Cassia
15165 N 138th Ln
1517 W Thomas Rd
152 Nunca St
1520 E Park Ave
1522 N Dorsey Ln
1522 N Freeman
1522 W Del Rio St
15222 W Windward Ave
15225 S 182nd Ln
15227 W Jackson St
1524 W Sahuaro Dr
15246 W Jefferson St
15251 W Tad Ln
15263 N 67th Dr
15273 W Roanoke Ave
1528 E Chilton Dr
1528 Iron Springs Dr
1528 Splinter Rock Way
1530 W Thompson Way
15305 W Roma Ave
1531 Laguna Palms Ave
1531 W Cindy St
15311 N 159th Dr
15315 W Pershing St
15318 N 138th Ln
1533 Bonnie Castle Way
1533 S Ponderosa Dr
1533 Tillman Falls Ave
15346 W Laurel Ln
15366 W Tasha Dr
15386 W Morning Glory St
1539 Misty Sky Dr
1539 S Loren Ln
154 Twin Towers Ave
1540 W Encanto Blvd
1540 W Mercer Ln
15411 W Hearn Rd
15432 S 7th Dr
15434 N Hana Maui Dr
15434 W Gelding Dr
1544 S Owl Dr
1544 Stone Valley Ave
15442 W Statler Cir
15448 N Cabrillo Dr
1545 E Glade Ave
15479 W Whitton Ave
155 E Cheyenne Rd
155 Mountainside Dr
155 Spinnaker Dr
1550 S Monterey St
15508 N 47th Pl
1552 S Roadrunner Dr
1552 Ward Frontier Ln
1554 N Christy Ln
1555 Wild Willey Way
15554 W Gelding Dr
156 Welland Ct
1561 E Elgin St
1563 Silver Falls Ave
15630 S 35th Way
1567 Homeward Cloud Ave
15672 W Mohave St
15685 N 102nd Way
15704 W Post Dr
15712 N 33rd Pl
1573 Homeward Cloud Ave
15733 W Smokey Dr
15739 N 172nd Ln
15743 W Rimrock St
1577 Pimlico Hills St
1578 Peaceful Pine St
1579 Comfort Hills St
1580 Rusty Ridge Ln
15808 E Jericho Dr
1581 E Shannon St
15813 W Morning Glory St
15817 E Palisades Blvd
15833 W Latham St
15848 N 48th Pl
15873 W Redfield Rd
15889 W Latham St
159 Afternoon Rain Ave
159 Castle Course Ave
159 Westminster Way
15900 W Post Dr
15923 N 89th Ave
15928 W Woodlands Ave
15946 W Linden St
1595 Darryl Ave
1598 Peaceful Pine St
15980 W Meade Ln
160 Horizon View Dr
1601 Lorna Dr
16026 S 13th Pl
16026 W Winchcomb Dr
16034 W Bartlett Ave
16035 S 9th Pl
1604 Wolf Canyon Ct
16048 W Desert Bloom St
1605 Los Alamos Dr
16056 N 25th Dr
1606 Chapman Dr
1606 Coyote Run Dr
16060 W Kendall St
1607 Chesterfield Ave
1608 Changing Seasons St
16080 W Jackson St
1609 E Del Rio Dr
1609 Gatewood Dr
161 Copper Rock Ct
161 Lenape Heights Ave
161 W Campbell Ct
16100 W Williams St
16118 W Miami St
1613 Crystal Chimes Dr
16137 N 159th Dr
1614 E Chanute Pass
1614 E Paradise Ln
1616 E Saratoga St
1618 Marathon Dr
16186 N 158th Dr
1619 Wendell Williams Ave
162 Castle Course Ave
16211 E Carmel Dr
16213 W Calavar Rd
16217 W Acapulco Cir
16218 W Superior Ave
1622 E Fremont Dr
1623 W Sparrow Dr
16230 N 99th Way
16231 E Bainbridge Ave
16231 S 13th St
16256 E Carmel Dr
1626 Clint Canyon Dr
16265 W Lupine Ave
16269 W Mercer Ln
1627 Cave Spring Dr
1628 Olive Palm Cir
1628 Ravanusa Dr
1630 Lorna Dr
1633 W Missouri Ave
1636 Linn Ln
1636 Mayfair Pl
16388 W Canterbury Dr
1641 Hartley Ave
1641 Sand Canyon Dr
16416 N Naegel Dr
16422 N 66th Dr
1644 Raindance Way
1645 Lefty Garcia Way
1649 W Pueblo Ave
165 Greenwich Village Ave
165 W Laurel Ct
16514 N 68th Dr
1652 Orange Daisy Pl
1652 Wendell Williams Ave
16522 E Morning Vista Ln
16529 W Grant St
16541 W Belleview St
1655 E Washington Ct
1656 Royal Canyon Dr
16573 W Marconi Ave
1659 N 114th Ave
16630 N 61st Pl
16633 N 153rd Dr
16638 N 168th Ave
16649 W Mescal St
1665 Britannia Ave
167 Desert Pond Ave
16705 W Tether Trl
16726 N 114th Dr
16790 W Fillmore St
168 Andada Dr
16800 W Southampton Rd
16809 W Central St
16828 S 13th Way
1683 Clovercrest Ct
16834 W Manchester Dr
1685 Butterfly Ridge Ave
1688 Crow Creek Ave
16909 W Mesquite Dr
1691 E Redwood Pl
1691 Ember Glow Cir
16917 N Briarwood Dr
1692 Butterfly Ridge Ave
1692 Duarte Dr
16921 W Rimrock St
16929 W Bristol Ln
1695 Leatherleaf Dr
1696 Mountain Song Ct
1697 Balsam Mist Ave
1699 E Maryland Ave
17 Soaring Bird Ct
170 Twin Towers Ave
1700 Desert Fort St
1700 Mexican Poppy St
1700 N Jones Blvd
17017 W Rimrock St
1703 Bamboo Rain Ave
1703 E El Parque Dr
1704 W Pelican Dr
1705 Double Arch Ct
1706 E Samuel Dr
1707 W Blue Sky Dr
1710 Sky Mountain Way
17108 E Salida Dr
1712 Crystal Downs Ave
17121 W Elizabeth Ave
1713 Eagle Peak Way
17130 E Oro Grande Dr
1716 Eagle Feather St
1716 Jack Rabbit Way
1716 W Minton St
1717 Chase Glenn Ct
17172 W Young St
1718 Sherwin Ln
1720 Bannie Ave
1720 Silver Birch Ln
1721 S Farmer Ave
1721 Sequoia Dr
17238 W Elizabeth Ave
1724 Buttermilk Dr
1724 Desert Fort St
17242 W Marshall Ln
1725 Pomerado Dr
1730 E Lehi Rd
1730 Franklin Chase Ter
17303 N 99th Pl
1731 Ashburn Dr
17313 W Saguaro Ln
1733 Buttermilk Dr
1736 Navajo Lake Way
1736 Sequoia Dr
1737 Chevrus Ct
1737 S 218th Ave
17380 W Pinnacle Vista Dr
1739 E Bluefield Ave
17406 W Banff Ln
1741 Howard Ave
1741 W Laurie Ln
17411 N Avelino Dr
1742 Ember Glow Cir
17427 W Lisbon Ln
17435 N 29th Ave
175 Wicked Wedge Way
17504 W Mauna Loa Ln
1751 W Roosevelt Ave
17586 W Eugene Ter
17590 N 114th Ln
17605 W Lundberg St
1762 Laurel Oak Dr
1762 Virgin Island Ave
1763 Yellowwood Dr
17634 W Mandalay Ln
17638 N 45th St
17648 W Buckhorn Dr
1766 Little Crow Ave
1767 E Carob Dr
177 Tad Moore Ave
17705 W Tonto St
17707 W Calavar Rd
17764 N 77th Pl
1777 S Balboa Dr
178 Augusta Course Ave
1780 W Canary Way
17827 W Hearn Rd
17836 W Lincoln St
17842 N 34th Dr
17842 N 49th Pl
17910 W Maui Ln
1792 Lily Pond Cir
17926 N 97th Pl
1794 W Desert Seasons Dr
1800 S Valley View Blvd
1801 E Buffalo St
18012 W Caribbean Ln
18017 W Caribbean Ln
1802 E Juniper Ave
18021 W Las Cruces Dr
1804 Cypress Bay Ave
1806 Versante Ave
1808 8th Pl
1809 E Broadway Rd
1809 Imperial Cup Dr
1811 Giant Pine Ave
18116 W Desert Ln
1815 Rapier Dr
1815 W Tuckey Ln
1816 Cameron St
18169 N 92nd St
1817 Drifters Peak St
1820 E Concorda Dr
1821 Walker Ln
1822 W Pollack St
18234 W Montecito Ave
18251 W Thunderhill Pl
1827 Grand Prairie Ave
1827 S 80th St
183 Paxon Hollow Ct
1832 Luna Alegre St
1833 E Patrick Ln
1833 Escondido Ter
1833 Luna Alegre St
1833 Midnight Wind Ave
1833 Sierra Hills Way
1834 E Dava Dr
1834 E Kings Ave
1836 Kassabian Ave
1837 Lyell Canyon Ln
1838 N 51st St
184 Laguna Hills Ct
1842 Muchacha Dr
18428 W Summerhaven Dr
1848 Quarley Pl
185 Bear Cove Ter
18508 W Sunbelt Dr
1851 E University Dr
1853 E Chilton Dr
18546 E Oak Hill Ln
1855 Indian Bend Dr
1856 Hollywell St
1857 E University Dr
1858 Mesquite Canyon Dr
186 Laguna Landing Dr
18650 N 1st Ave
18656 N 70th Ave
1867 Mesquite Canyon Dr
1869 Canvas Edge Dr
187 E Carob Dr
1871 Granemore St
1871 Via Delle Arti
1872 E Omega Dr
1872 Walker Ln
1874 E Brentrup Dr
1874 Versante Ave
1876 E Barnacle Ave
188 Fairway Woods Dr
18807 N 17th Ave
1882 Hillsboro Dr
1887 Eagle Flight Ln
18901 E Superstition Dr
1891 Eagle Flight Ln
18913 N 69th Ave
1892 Silver Whisper Ave
18930 E Superstition Dr
1896 S 225th Ave
19 Megan Dr
190 Tayman Park Ave
1900 Realeza Ct
19017 N Welk Dr
1904 Bocale Ct
1904 Peyton Stewart Ct
1905 Trail Peak Ln
1907 Davina St
1907 S Tucana Ln
1908 Golden Horizon Dr
1909 E Smoke Tree Rd
191 Mountainside Dr
1910 Featherbrook Ave
1912 Placid Ravine St
1914 W Holly St
1917 E Gemini Dr
1918 E Palmcroft Dr
192 Fortress Course Ct
1924 Westwind Rd
1926 E Marquette Dr
1926 E Richards Dr
1927 E Wesleyan Dr
1928 E Jacinto Ave
1929 Evelyn Ave
1929 Granemore St
1932 E Auburn Dr
1933 E Winchester Pl
1935 E Campo Bello Dr
1935 Joyful St
1940 E Huntington Dr
1941 E Inverness Cir
1943 E Torrey Pines Ln
1949 E Bellflower Ct
1951 Arabian Ct
1953 E Citation Ln
1958 W Meadow Dr
196 Broken Putter Way
196 Genesee Point St
1960 E Fremont Dr
1960 Joyful St
1963 Orchard Mist St
1966 E Browning Pl
1970 Salvation St
19721 E Emperor Blvd
1976 Galleria Spada St
1977 Lorca Ct
1978 Morro Vista Dr
1979 Ardilea St
198 Mount Earl Ave
198 Winnsboro St
19808 N Concho Cir
19863 N 84th St
1990 Songbird Ct
19929 N 77th Ave
19993 N Matilda Ln
20 Desert Gallery St
20 E Hermosa Dr
20 Olive Tree Ct
20 Princeville Ln
200 Boothbay St
2001 Winwood St
2002 E Sweetwater Ave
20036 N Coyote Lakes Pkwy
2005 Denby Ave
2007 Yosemite Ct
2008 Waterbury Ln
2009 N 17th Ave
201 E Duke Dr
201 W Alegre Dr
2010 N 37th Pl
2010 W Monte Vista Rd
2011 E Catclaw St
2012 Ardilea St
2012 Poetry Ave
2013 Loggerhead Rd
2013 Madagascar Ln
2015 Granemore St
2015 W Davis Rd
2016 Trailside Village Ave
2020 W Cactus Rd
20209 N 55th Ave
2021 W Hayward Ave
2022 W Joan De Arc Ave
2024 N 81st Pl
2024 Summit Pointe Dr
2025 E Anderson Dr
2025 S Granada Dr
2027 Cape Cod Landing Dr
20279 N 52nd Dr
2031 S Palmer Cir
2036 Wandering Doe Ln
20361 N 89th Dr
204 Delamar St
204 Tainted Berry Ave
204 Thurston St
2041 E Granite View Dr
20414 N 9th St
2042 N 77th Dr
2043 Fred Brown Dr
20436 W Terrace Ln
2044 Havelina St
20480 W Point Ridge Rd
2049 W Hayward Ave
20490 N 80th Ave
205 Junction Peak Ave
205 Surtees Point St
205 Woodley St
2053 Smoketree Village Cir
2055 Bledsoe Ln
2057 Lordsburg Ln
2059 Club Crest Way
20642 N 38th Dr
207 W Wickieup Ln
2071 W Harrison St
20711 W Stone Hill Rd
2073 Brassy Dr
2073 Madica Ave
2077 Hocus Pocus Pl
20789 W Maiden Ln
208 Emerald Vista Way
208 Gemstone Hill Ave
208 Popolo Dr
20806 N 52nd Ave
2081 Hocus Pocus Pl
20813 N 39th Dr
2085 E Buena Vista Dr
2092 Crowley Way
2095 Culmination Ln
2095 Desert Prairie St
20968 N 80th Dr
20985 E Sonoqui Dr
20990 N 66th Ln
2104 Merganser Ct
2105 Arpeggio Ave
2105 Shadow Canyon Dr
21051 W Court St
2108 N 39th Ave
2108 W Georgia Ave
211 Arbour Garden Ave
2111 Lady Frances Ln
2111 Lost Maple St
2113 S Nielson St
2115 Falcon Crest Ave
21161 E Stonecrest Dr
2118 Edgewood Ave
2119 N 68th Pl
2119 W Hayden Peak Dr
2120 Armadale Dr
2120 Van Patten Pl
21206 W Granada Rd
2121 S Ventura Dr
2124 Crooked Pine Dr
2127 Audrey Hepburn St
2129 E Mallard Ct
213 Meyers Ave
213 Upland Blvd
2130 S Buffalo Dr
2130 Spring Water Dr
2133 Merganser Ct
2134 W Le Marche Ave
2135 Gunnison Pl
2135 W Maldonado Rd
214 Luninborg St
214 W Desert Ln
2140 Calcite Cliff Ave
21404 W Monte Vista Rd
2141 W Utopia Rd
2144 Marywood Park Ct
21447 N 29th Dr
2145 Mountain City St
2147 W Mulberry Dr
2148 E La Donna Dr
215 Meyers Ave
2150 Lone Desert St
2151 Casa Ladera St
2152 N 30th St
2156 Chapman Ranch Dr
2159 Enfield Cir
216 Abundance Ridge St
216 Chiquis Ct
216 Roman Empire Ave
216 Thunder St
2160 Spurs Ct
2160 Sunset Vista Ave
21619 W Durango St
2162 Haypenny Ct
2162 W Myrtle Dr
21635 N 29th Dr
21639 E Camina Plata
2167 Handel Ave
2169 Eagle Watch Dr
217 Belmont Canyon Pl
2174 Hearts Club Dr
2174 S Heron Ln
2180 Hearts Club Dr
2183 Waterton Rivers Dr
2192 Sawtooth Mountain Dr
2197 Eaglecloud Dr
2198 Brighton Point Ave
2199 W Renaissance Ave
22 Alyson Pond Cir
220 Belmont Canyon Pl
220 Red Cloud Ter
220 Serenity Crest St
2200 Jeanne Dr
2201 E Yuma Ave
2201 San Jose Ave
22016 N 66th Ln
2202 W Pinkley Ave
2204 Alia Ct
2204 Isabelle Ave
22056 W Yavapai St
2209 N 135th Dr
221 S Olive
2211 S Taylor Dr
2212 Glen Heather Way
2212 Valley Dr
2213 S Cherry
2216 E Devon Ct
2216 E Eugie Ter
2217 Diamondville St
2217 Ladue Dr
2217 N Jones Blvd
2217 White Mist Dr
2219 Allegiance Dr
222 Genesee Point St
2220 Maple Rose Dr
2220 Midvale Ter
2220 Patriotic Ln
2222 S 83rd Dr
2223 Sawtooth Mountain Dr
22231 N 29th Dr
2224 E Kelton Ln
2224 N 27th St
2224 W Nancy Ln
22269 W Tonto St
2227 Ramsgate Dr
2229 Warm Walnut Dr
2230 Driftwood Tide Ave
2233 E Nathan Way
2234 Diamondville St
2234 Tulip Tree St
22343 W Hadley St
2236 Cordaville Dr
2239 Bensley St
2239 Sandstone Cliffs Dr
2240 Shadow Canyon Dr
22407 S 211th Way
2241 Juniper Berry Dr
22410 N 53rd Pl
2242 E Desert Inn Rd
2242 N 12th St
2242 W Peak View Rd
2248 Summer Home St
2249 S Evergreen Rd
225 Spur Ranch Ave
2251 E Hacienda Ave
2252 Aragon Canyon St
2256 Daley St
2257 E Peach Tree Dr
2258 Green Mountain Ct
226 Hanley Way
2260 W Hayden Peak Dr
2262 E Beachcomber Dr
22669 W Cocopah St
2267 Heavenly View Dr
2268 Tomlinson Ln
227 Greenbriar Townhouse Way
227 Serenity Crest St
227 Spectacular St
227 W Darrow St
2273 Georgia Pine Ct
22743 W Yavapai St
22787 W Mohave St
228 E Canyon Way
228 Friendly Ct
228 Silver Castle St
22836 W Yavapai St
2284 Malaga Peak St
22843 W Mesquite Dr
2289 E Palm Beach Dr
2293 Aragon Canyon St
23009 W Cocopah St
2301 E Sylvia St
2305 E Mitchell Dr
2305 Pearson Ct
2306 E Toledo Pl
2307 Summer Home St
2308 N 28th Pl
2309 Chatfield Dr
2309 Hot Oak Ridge St
2309 S College Ave
2309 S Grandview Ave
2309 Tinsley Ct
2309 W Carter Rd
231 Night Fall Ter
2311 E Silverwood Dr
2312 Bloomington Dr
2312 Pine Bluff Ct
2312 S Oak St
2312 Sky Island Dr
2313 Maverick St
2313 S Grandview Ave
2316 N 72nd Pl
2316 Prometheus Ct
2317 Martinique Ave
2317 N Mitchell St
2319 E Taro Ln
232 Hillcrest Dr
232 Stormson Ct
2320 Mohigan Way
2320 Silvereye Dr
2321 S Karen Dr
2321 W Cabana Cir
2321 W Hartford Ave
2325 Ramsgate Dr
2327 Hillstone Ave
2332 S Lynch
2334 Jada Dr
2335 Schaeffer Hills Dr
2335 W Nopal Ave
2338 N 52nd St
2339 Peaceful Sky Dr
2339 W Northern Ave
2341 Moorpark Way
2344 W White Feather Ln
23456 N 40th Ln
2346 E Poinsettia Dr
2348 Martinique Ave
2348 Viewcrest Rd
2349 E Betty Elyse Ln
2349 Sterling Heights Dr
2351 E Azalea Dr
2352 Peaceful Moon St
2361 E Huntington Dr
2365 S Hiscox Ln
23695 W Chambers St
237 W Sequoia Dr
2375 Cliffwood Dr
238 W Atlantic Ave
2381 Carnegie Hall St
23851 W La Salle St
2387 N 142nd Ave
2390 Malaga Peak St
2390 W Allens Peak Dr
2393 Aztec Ruin Way
23955 W Antelope Trl
23959 W Antelope Trl
2396 Seagate Ct
2398 Predera Ave
24 Cool Days Ave
24 Hatten Bay St
240 E Muriel Dr
240 Elkins Cir
2401 W Alice Ave
2402 Endearing Ct
2402 Legacy Island Cir
2402 W Running Deer Trl
2404 Dutchmans Pipe Ct
2404 W Roeser Rd
2405 Crane Ct
2407 Predera Ave
2407 W Crimson Ter
2408 Carnegie Hall St
2409 Sierra Heights Dr
24092 N 165th Ln
2410 Character Ct
2410 N 38th Pl
2412 Taragato Ave
2414 S 236th Dr
2414 W Devonshire Ave
2415 Eagle Harbor Dr
2415 W Maldonado Rd
2416 Weaverville Dr
2419 Predera Ave
2422 Ember Mist Ct
2423 S 84th Gln
2424 Belt Buckley Dr
2424 Ginger Lily Ln
243 N Sandal
2431 E Mescal St
2431 W Gaby Rd
2432 Granada Bluff Ct
2433 E Nathan Way
2434 E Jacinto Ave
2439 E Dust Devil Dr
2439 W Gaby Rd
244 W Oraibi Dr
24401 N Lost Dutchman Way
2441 Desert Glen Dr
24466 W Pueblo Ave
2448 Kaymin Ridge Rd
2454 S 88th Ln
2456 Carnegie Hall St
2458 Avenida Sol
246 Summit Vista St
2460 Avenida Cataluna
24613 W Gregory Rd
2464 Muirfield Ave
2467 Sheltered Meadows Ln
247 Rustic Club Way
2475 Kaymin Ridge Rd
2476 Serene Moon Dr
24805 W Rosita Ave
24818 W Huntington Dr
2485 April Breeze Ln
2485 S Marble St
2488 Comet Cloud Ct
2491 Venarotta St
2496 Grassy Spring Pl
250 N Nash Way
250 Rolling Springs Dr
2500 Citrus Garden Cir
25001 W Dove Mesa Dr
2505 E Michigan Ave
2505 Soldier Creek Ct
2509 Springville Way
251 Queens Ct
2510 Country Orchard St
2510 Gardenia Flower Ave
2514 W Lane Ave
2515 E Villa Maria Dr
2515 New Salem Ave
2517 Kirkmichael Ln
2517 N 86th St
2517 Palmridge Dr
25176 W Cranston Pl
2518 E Harmony Ave
2519 Castlesands Way
252 Quail Ranch Dr
2522 Palace View Dr
2523 S Jefferson
2524 McCarran St
25242 N 40th Ln
2525 E Corrine Dr
2525 Tumble Brook Dr
2526 E Meadow Land Dr
25261 W Cranston Pl
2528 W Belmont Ave
253 Mesquite Ridge Ln
2530 E Fairmount Ave
2530 E Mine Creek Rd
2532 W Morten Ave
2532 Willow Wren Dr
2534 W Red Fox Rd
2538 Ontario Dr
25393 W Clanton Ave
25395 W Clanton Ave
25399 W Lincoln Ave
2540 Serenity Hollow Dr
25409 W Clanton Ave
2541 Ontario Dr
2541 Sungold Dr
25412 N 40th Ln
25417 W Clanton Ave
2542 Evening Twilight Ave
25455 S Truro Dr
2549 Sable Ridge St
255 Fairway Woods Dr
2551 Misty Olive Ave
2555 Paradise Village Way
2556 Sable Creek St
256 Fairway Woods Dr
2560 Sable Creek St
25619 W Satellite Ln
25645 S Ontario Dr
2565 W Woburn Ln
2568 Corner Stone Cir
2573 E Southwood Rd
2573 Pont Marie Dr
25817 W Winslow Ave
2582 W Kit Carson Trl
25823 N 41st Way
25841 W Kendall St
2587 Darda St
259 Newelton Ct
2590 Woodson Ave
260 Pastel Cloud St
2600 Orchard Meadows Ave
2600 Peat Moss Ave
2601 Amber Crest St
2603 Summerview Pl
2605 Bottle Palm Ct
26077 W Sequoia Dr
2612 Fading Mist Dr
2616 Island Brook Dr
2617 Ground Robin Dr
2617 Rainbow Cactus Ct
2622 E Paradise Ln
2624 N 86th Dr
2624 W Orangewood Ave
2626 N 46th St
2627 S Torrey Pines Dr
2629 Ironside Dr
2631 Country Mile Dr
2632 E Libby St
2635 Cottonwillow St
2637 Lotus Hill Dr
2637 S Harmony Ave
2638 E Bear Creek Ln
264 Aspen Knoll Dr
264 E Ashurst Dr
2640 White Pine Dr
26400 N 107th Way
2647 Lochleven Way
265 Blackstone River Ave
2653 Langford Ave
2662 Churchill Cir
2663 E Del Rio St
2668 Wild Ambrosia Ave
26744 N 176th Ln
268 Single Petal St
26807 N 84th Ave
2685 Park Creek Ln
2685 Virgo Dr
2690 Heathrow St
26902 N 83rd Gln
2691 Lochleven Way
2694 Iris Point Way
270 E Indigo Dr
2700 Prism Cavern Ct
2701 Port Lewis Ave
2705 Howard Dr
2706 Peekskill Ave
271 Tungsten St
2710 Frecco Cavern Ct
2710 Hammetts Landing Walk
2713 Duck Pond Ct
2715 Hammetts Landing Walk
2717 Cloudsdale Cir
2718 S 113th Ave
272 Green Peace Ct
272 Morning Crest Ave
2721 E Bart St
2722 E Galveston St
2724 Quail Roost Way
2728 Briarcliff Ave
2728 Herons Creek Dr
2728 Lotus Hill Dr
2729 Valley Downs Dr
273 New River Cir
2732 Berg St
2735 S Milburn
2735 W Royal Palm Rd
2737 E Shannon St
2738 Auchmull St
274 Timber Hollow St
2744 Knoll Point St
2747 E Chipman Rd
2747 Lochleven Way
2748 Chaucer St
2748 Pinewood Ave
2750 Pala Dura Dr
2751 E Vermont Dr
2751 Rebano St
276 E Coconino Dr
27602 N 89th Ln
2763 White Sage Dr
2769 Showcase Dr
2774 Sorrel St
2779 Culloden Ave
2781 Eldora Cir
2785 Audra Faye Ave
2785 E Jasper Dr
279 Fairway Woods Dr
27910 N 66th Ln
2794 Glen Port St
2801 Bahama Point Ave
2801 Via Bel Mondo St
28018 N 92nd Ave
2804 Briar Knoll Dr
2804 Kinknockie Way
2808 Crystal Lantern Dr
2808 W Orangewood Ave
2809 Sterling Cove Dr
281 Finsbury Ct
2812 Dotted Wren Ave
2813 Emily Ann Ct
2816 Albrook Cir
2816 E Megan St
2816 Tanagrine Dr
2819 E Marconi Ave
2820 King Michael Ave
2820 N 86th Dr
2821 E Cherry Hills Dr
2821 Norfolk Ave
2823 Disk Ave
2823 Sapphire Desert Dr
2824 E Megan St
2825 Barrel Cactus Dr
2825 Dawn Crossing Dr
2827 Mill Point Dr
2828 Autumn Haze Ln
2831 Canonero St
2831 Dalsetter Dr
2831 Shannon Cove Dr
28317 N 61st St
2834 E Kathleen Rd
2834 Evening Rock St
2836 Tilten Kilt Ave
2839 Dawn Crossing Dr
2839 E Le Marche Ave
2839 E Montecito Ave
284 Fair Play St
2840 Blythswood Sq
2840 Kinknockie Way
2840 S Coyote Canyon Cir
2842 Briar Knoll Dr
28437 N 112th Way
2849 Bellini Dr
2849 Canonero St
2850 Maryland Hills Dr
28515 N 25th Ave
2855 Mountain Mist Ct
2858 Marathon Dr
286 Fairmeadow St
2860 E Megan St
28621 N 64th Dr
2864 Meadow Park Ave
2866 Destino Ln
2867 Tori Way
2868 Rothesay Ave
2870 E Serene Ave
28713 N 148th St
2872 Glass Vine Ct
2875 Hedge Creek Ave
2875 Starling Summit St
2876 S 160th Ln
2877 Kinknockie Way
288 Sweet Sugar Pine Dr
2890 Belcastro St
2892 Desert Zinnia Ln
28945 N Tsavorite Rd
2901 Abercorn Dr
2901 E Osborn Rd
2901 S Tumbleweed Ln
2902 W Irma Ln
2904 E Verbena Dr
2904 Sarina Ave
2907 Crackling Leaves Ave
2907 E Michelle Dr
2907 Tremont Ave
2909 Cape Verde Ln
291 Waterton Lakes Ave
2912 Demetrius Ave
2913 Hot Cider Ave
2914 Lindell Rd
2916 E Cobre Dr
2916 Paradise Hill Ct
2917 Big Mountain Ave
2917 Pumpkin Harvest Ave
2918 Crisp Wind Ct
2919 N Athena
2920 Whispering Wind Dr
2921 Harewood Ave
2924 Channel Bay Dr
2926 N 108th Ave
2927 Tremont Ave
2929 E Fandango Dr
2932 S El Paradiso
2933 E Dunbar Dr
2940 Carmelo Dr
29409 N 53rd St
2943 W Thorn Tree Dr
2944 N 26th St
2955 S Del Rancho Cir
297 Fox Lake Ave
2978 E Glenhaven Dr
2983 Ferndale St
2983 Scenic Valley Way
29843 W Clarendon Ave
2986 Harbor Heights Dr
2986 N 147th Dr
2993 Formia Dr
2999 Reiger Ct
3 Brown St
30 Anthem Creek Cir
300 E Broadway Rd
3001 Lotus Hill Dr
3001 Merritt Ave
3001 Sandbar Ct
3001 Treasure Island Rd
30025 N 128th Ave
30037 N 77th Pl
3004 Battle Point Ave
3004 Bicentennial Pkwy
3007 Sunrise Bay Ave
3007 W Villa Maria Dr
3008 N 40th Ave
301 Turtle Peak Ave
3010 E Columbus Ave
3010 W Languid Ln
3011 Bradford Hill Ave
3011 E Delta Ave
3011 Stratmoor Hills Ave
3012 Jacaranda Dr
3012 Maple Valley St
3012 W Irma Ln
3013 Marsh Ct
3013 Sungold Dr
3013 W Paradise Ln
3015 Big Green Ln
3015 W Lone Cactus Dr
3017 E Hampton Cir
3019 S 101st Ave
3021 E Siesta Ln
3021 S 89th Dr
3022 S Cortland Cir
3022 San Mamete Ave
3023 Taranto Heights Ave
3024 Misty Harbour Dr
3025 Tularosa Ln
3029 Dowitcher Ave
3029 W Maryland Ave
3032 S 94th Ave
3036 Gentle Breeze St
3037 Monroe Park Rd
3038 Nordoff Cir
3039 S Mojave Rd
304 N 56th Pl
3040 Ocean View Dr
3044 Paseo Hills Way
30447 N 152nd St
3045 Balcones Fault Ave
305 E Vine Cir
305 Prince Charming Ct
305 Queen Creek Cir
305 W Wahalla Ln
3056 Brownbirds Nest Dr
3056 Camino Sereno Ave
3060 E Russell St
3060 W Patrick Ln
3061 Yankee Clipper Dr
30614 N 45th Pl
3075 W Yellow Peak Dr
30789 N 125th Dr
3097 Camino Sereno Ave
3099 Maple Ridge Ct
310 Clover Glen Ct
3101 E Carey Ave
3101 W Clinton St
3105 S Harl Ave
3106 S Dromedary Dr
3108 W Mark Ln
311 Grassy Pines Ct
311 W Wisteria Pl
3112 Twilight Crest Ave
3115 W Maryland Ave
3119 Diamond Crest Ln
3120 Winter Sunset Ave
3121 Morning Whisper Dr
3122 Mastercraft Ave
3124 Amari Ave
3126 Meadow Flower Ave
3128 Biscayne Springs Ln
3129 Little Crimson Ave
313 Autumn Palace Ct
313 W Hereford Dr
31301 N Cavalier Dr
3133 Bel Air Dr
3135 Lido Isle Ct
3135 N 28th St
3137 Cooper Creek Dr
3137 Nevelson Walk
3139 Dalmazia Ave
3139 Strawberry Park Dr
3142 Belvedere Dr
3142 W Potter Dr
3143 E Patrick St
3153 Monet Sunrise Ave
3155 E Desert Ln
316 Sonoma Valley St
316 W Northern Ave
3163 W Stephens Pl
3164 Chambord St
317 Palisades Dr
317 Snow Dome Ave
3173 Elk Clover St
3175 Obscured Light Walk
3178 Swallow Ln
318 Palm Trace Ave
318 W Georgia Ave
3186 Castle Canyon Ave
3188 Mist Effect Ave
319 E Riviera Dr
3191 E Lark Dr
3192 Baffetto Ct
3192 Mist Effect Ave
3197 Dusty Moon Ave
320 Island Reef Ave
320 N 20th Ave
3202 W Pecan Rd
32030 N 20th Ln
3207 W Michigan Ave
3208 W Surrey Ave
3209 Monaco Shores Dr
3209 W Robin Ln
321 Maddelena Ave
3210 E Siesta Ln
3210 S Mingus Dr
3214 N 70th St
3215 W Abraham Ln
3216 Carefree Beauty Ave
3216 Malibu Vista St
3216 Medicine Man Way
3216 River Glorious Ln
3217 Bermuda Bay St
322 Brent Ct
322 Quiet Harbor Dr
322 Sweetspice St
3220 Mystic Ridge Ct
3220 N 79th Ave
3222 W Rapalo Rd
3225 W Leisure Ln
3227 W Dancer Ln
3228 Dragon Fly St
3228 Ivory Coast Dr
3232 W Alta Vista Rd
3235 Daffodil Ridge Ave
3235 W Bajada Dr
3238 E Macaw Ct
3238 W Angela Dr
324 N 90th St
3241 Bishop Pine St
3248 N 84th Ave
3249 Haven Beach Way
325 Cavalla St
325 Montessa Ave
3253 Little Stream St
3256 E Isaiah Ct
3260 River Glorious Ln
328 Coral Fountain St
3280 N Heritage Way
3285 E Meadowview Dr
329 Warmside Dr
3299 E Loma Vista St
3301 S Terrace Rd
3305 Fernbird Ln
33070 N Cat Hills Ave
33096 N Kari Rd
331 Laguna Glen Dr
33105 N 23rd Ave
3313 Cheyenne Gardens Way
3315 E Jasper Dr
3316 E Orchid Ln
3316 Hyannis Cir
3317 Ventana Hills Dr
332 E Malibu Dr
332 View Dr
3320 Summerfield Ln
3327 W Joan De Arc Ave
3331 E Calypso Ave
3331 S Shafer Dr
3336 N Park St
3336 S Pine St
3339 Dragon Fly St
3344 N Stone Gully
3347 E Windsor Ave
3349 Sabino Canyon St
3355 Halter Dr
3355 Jasmine Vine Ct
3357 China Dr
3357 W Potter Dr
3357 Wayward Ct
3359 Zephyr Ct
3360 Athens St
3365 Eagle Bend St
3365 Edenville Dr
3365 Parma Galleria Ave
3367 E Bluejay Dr
3368 Mountain Bluebird St
3373 Osiana Ave
3377 Ewa Beach Dr
3378 Seneca Dr
338 Dog Leg Dr
338 Glistening Cloud Dr
338 Island Reef Ave
338 Pleasant Summit Dr
3380 N Bronco St
3382 Syvella Ct
3388 Alcudia Bay Ave
340 S Mallard St
340 Silverado Pines Ave
340 Sweet Pea Arbor St
3402 Midnight Moon St
3404 White Bark Pine St
3405 Brayton Mist Dr
3409 Amish Ave
3411 Holly Ave
3412 Avalon Ave
3412 El Cortez Ave
3412 Lonesome Drum St
3413 Fledgling Dr
3413 W Seldon Ln
3414 N Navajo Trl
3419 E Angela Dr
3420 Strawberry Roan Rd
3420 Trilogy Dr
3421 W Del Monico Ln
3422 E Avalon Dr
3423 E Escuda Rd
3423 Middle View Dr
3423 W Bloomfield Rd
3426 E Hillery Dr
343 Perry Ellis Dr
343 River Glider Ave
3431 E Russell St
3432 Miramar Dr
3433 E Renee Dr
3435 Villa Knolls South Dr
3435 W Country Gables Dr
3436 Silver Bridle Pl
3436 W Malapai Dr
3436 Yountville Ct
3438 W Mauna Loa Ln
3440 Summersprings Dr
3441 Martin Hall Dr
3444 E Betsy Ln
3446 E Avalon Dr
345 Sweet Pea Arbor St
3454 Whitman Falls Dr
3459 Blue Heather Dr
3460 Victory Ave
34614 N 30th Dr
3463 Spencer St
3464 Abilene Gold Ct
3465 Don Miguel Dr
3465 Manzano Cir
34811 N 52nd St
34827 N 30th Ave
34828 N 92nd Pl
3496 E Milky Way
35 N 123rd Dr
35001 N 30th Dr
3501 S Nebraska St
3502 E Evans Dr
3505 Saint Nazaire Ave
3507 W Mandalay Ln
3508 E Oraibi Dr
3508 Ponza Ct
3509 Kendall Point Ave
351 Arbour Garden Ave
351 Seine Way
3510 E Edna Ave
3512 E Hearn Rd
3516 Carisbrook Dr
3519 E Pinot Noir Ave
3526 E Montecito Ave
3526 S Shafer Dr
3526 W Sierra St
3526 W Tulsa St
3528 Bagnoli Ct
3528 W Saguaro Park Ln
353 Lander Ter
3532 Arcata Point Ave
3532 Harbor Tides St
3532 Nantova Ct
3532 Perching Bird Ln
3532 Villa Knolls North Dr
3535 E Calistoga Dr
3538 E Gold Dust Ave
3538 Pueblo Way
3540 E Pinot Noir Ave
3540 Trotting Horse Rd
3541 E Eleana Ln
3541 W Vernon Ave
3542 W Plymouth Dr
3544 S Jasmine Dr
3548 Terraza Mar Ave
3549 Remington Grove Ave
355 Brilliant Summit Cir
355 N 85th Pl
3550 W Willow Ave
3551 Judah Way
3552 Warmbreeze Way
356 John Henry Dr
3571 E Gleneagle Pl
3593 Pinnate Dr
36 W Pasadena Ave
360 E 6th Ave
3601 W Country Gables Dr
3602 E Long Lake Rd
3602 W Ruth Ave
3602 W San Juan Ave
3607 Sanwood St
3609 Rainy River Rd
3610 W Camino Del Rio
3613 Deer Flats St
3613 Riviera Ave
3614 E Taro Ln
3618 E Montecito Ave
3619 American Pie Ct
362 E Daniella Dr
3621 E Hyatt Ln
3621 Wild Willow St
3622 Dutchmans Vine Ct
3622 Pinnate Dr
3623 W Morse Ct
3625 E Orchid Ln
3625 Sanwood St
3625 W San Juan Ave
3628 Kingfishers Catch Ave
363 Ladies Tee Ct
3633 W Eastman Ct
3634 Vino Rosso Ave
3638 Extreme Ct
3639 Ambergate Ct
3642 Icon St
3643 Wild Springs St
3644 E Rakestraw Ln
3644 W Campo Bello Dr
3645 Lakeside Villas Ave
3646 E Montecito Ave
3649 Sanwood St
3649 Sesto Ct
3650 E Leslie Dr
3650 W Carlos Ln
3651 E Leslie Dr
3651 S Ivy Way
3652 Breman St
3653 W Saragosa St
366 W Corriente Ct
36608 N 51st St
3666 Villa Knolls South Dr
3669 Lucky Horseshoe Ct
3670 Wild Springs St
3671 Wild Springs St
3673 Largo Verde Way
3679 S Riley St
3681 Sanucci Ct
3689 Steinbeck Dr
3698 Casellina Ct
37 Mesquite Village Cir
37 Misty Springs Ct
370 Manti Pl
3701 Shanagolden St
3704 Bronco Billy Ct
3704 Via Geneva
3712 E Earll Dr
372 Cart Crossing Way
372 Sunward Dr
3720 Crellin Cir
3720 S 54th Gln
3721 N 125th Dr
3722 True Spring Pl
3722 Wild Lily Ct
3724 Tiffin Ct
3725 Bonanza Cir
3725 Bronco Billy Ct
3725 Sorrowing Sparrow Ct
3726 Blake Canyon Dr
3727 E Trinity Ln
3728 E Monterosa St
373 Banff Ct
3732 Honey Crest Dr
3732 White Quail Ct
3736 E Morrow Dr
3736 W Villa Maria Dr
3736 W Villa Theresa Dr
3737 Capsule Dr
3737 Konica Ct
3737 Prosperity Ln
3738 W Claremont St
3739 E Trinity Ln
3741 Grand Viewpoint Ct
3741 S Oxley
3742 Horseshoe Mesa St
37439 W Merced St
3745 W Sierra St
3748 Crest Horn Dr
3749 Garden North Dr
3749 N Rowen
3752 Yorba Linda Dr
3754 Emerald Bay Cir
3763 Topawa St
3766 Lipan Point St
3767 Darren Thornton Way
3770 Paria Canyon St
3771 Bella Legato Ave
3772 Crest Horn Dr
3774 Decade St
3776 Lodina Ct
3776 Port Ritchey St
3782 Bossa Nova Dr
379 Manti Pl
3791 Lodina Ct
38 Desert Highlands Dr
3802 N Sawtooth
3805 Van Ness Ave
3811 E Devonshire Ave
3811 Fahrenheit Ct
3814 Stadium Ave
3818 E Dahlia Dr
3819 E Crest Ln
3820 W Quail Ave
3821 E Horseshoe Pl
38269 N Jonathan St
3828 E Gideon Way
3829 W Butler Dr
3830 S Thistle Dr
3830 W Royal Palm Rd
3831 Trellis View Ave
3832 Autumn America Pl
3832 Mountain Waters St
3832 Van Ness Ave
3834 W Ashton Dr
3837 E Robert St
3839 Palm Island Ct
3840 Fitzpatrick Dr
3844 Windansea St
3846 Falcon Springs Dr
3848 Fitzpatrick Dr
385 Dog Leg Dr
3850 W Lamar Rd
3851 Hildebrand Ln
3854 Biltmore Bay St
3855 E Sophie Ln
3855 Waynesvill St
3856 Maryland Ave
3857 Placita Del Lazo
3858 Placita Del Lazo
3874 Steinbeck Dr
388 Gracious Way
388 S 228th Ln
3890 Steinbeck Dr
38916 N 23rd Ave
3893 W Chicago St
39 Vicolo Della Luna
390 N 14th St
3902 W Chicago St
3906 N 191st Ave
3909 S Nebraska St
3911 E Corrine Dr
3912 S Emery
3913 E Sophie Ln
3914 S 52nd Ln
3916 E Marlene Dr
3916 Pia Rosetta St
3918 S Napa Ln
3927 S Illinois St
3930 S Nebraska St
3931 S Laurel Way
3933 Herford Ln
3938 Mountain Birch St
3943 N 65th St
3943 S Crosscreek Dr
3944 Free Bird Crest Ave
3947 Keasberry Ave
3948 Applecrest St
3948 Dusty Coral St
3948 E Earll Dr
3949 Arrowood Dr
395 Chadwick Cir
395 Foster Springs Rd
3951 Jontue St
3952 S Napa Ln
39522 N Gold Mine Ln
3958 Topawa Dr
3960 Welsh Pony St
3961 Candleglow Ct
3961 Tangerine Ct
3969 Button Creek Ct
3969 Fire Fox Dr
3969 Jazzy Ginger Ct
397 Hidden Hole Dr
10 Via Visione
1011 Leadville Meadows Dr
1012 Eric Stocken Ave
10169 Maidens Wreath Ct
10186 Crepe Myrtle Ct
1022 Hyperion Dr
1023 S San Vincente Ct
1029 E Fairmount Ave
10322 Charlottsville Ct
10630 E Jensen St
10873 Paradise Rd
10889 Osage Winter St
10939 Sadlers Wells St
1107 Via Barcelona
11152 African Sunset St
11161 Abbeyfield Rose Dr
1135 S Judd St
1136 Via Degli
1157 Appaloosa Hills Ave
116 Cable View Ave
116 S Lebaron
11769 San Rosarita Ct
1180 Via Trevi
119 Serramonte Ct
1202 Granite Ash Ave
1217 S Farmer Ave
1246 E Daisy Way
130 Bel Port Dr
1313 Spice Ridge Ct
13300 E Via Linda
13450 E Via Linda
1348 E Broadmor Dr
1359 Grass Creek Ave
1367 State Rte 87
1405 State Rte 612
1407 Pathfinder Rd
1421 Evans Canyon Ct
145 Voltaire Ave
1464 Harmony Hill Dr
148 Desert Bell Way
15 Via Mantova
15 Via Visione
1527 Pen Hollow Ct
1595 Ward Frontier Ln
160 Bel Port Dr
1604 Box Step Dr
16342 E Dixileta Dr
166 Lovett Rd
1733 E Tanya Rd
1786 Amarone Way
181 Bel Port Dr
1846 N 51st St
18517 E Via De Palmas
1854 Musket Way Dr
1881 W Alexander Rd
1885 Apricot Ct
1886 Via Firenze
19 Via Visione
1914 W Yellowstone Way
1916 Flower Hill St
1924 Gifford St
1940 W Yellowstone Way
1945 Simmons St
2 Biltmore Estates Dr
2 Rue De Chateau Pl
2013 Via Firenze
2020 Pipeline Beach Ct
2050 W Warm Springs Rd
2071 Via Firenze
210 E Flamingo Rd
2104 Del Aqua Ave
2116 Port Antonio Ct
212 Boothbay St
2157 Arpeggio Ave
2305 Pearson Ct
2318 W Via Perugia
2321 Black River Falls Dr
24 Via Vasari
2401 Paveene Ave
2402 W Lewis
2486 Rye Beach Ln
249 S Hobson
2501 W Lewis
2556 Lazy Saddle Dr
256 Camino Viejo St
258 Camino Viejo St
2585 Amazing Meadows Ave
2607 Pebblegold Ave
2641 Rue Toulouse Ave
269 Via Contata St
2709 Kindness Ct
2725 State Rte 612
27520 N 174th St
2753 Laguna Seca Ave
2755 E Dry Creek Rd
2791 Fountain Ridge Ln
285 Broadcast Ave
2862 Via Firenze
2864 Via Firenze
289 Linn Ln
291 Red Eucalyptus Dr
2915 Paradise Hill Ct
30 Via Mantova
3008 Via Venezia
3016 Via Contessa
3019 State Rte 562
31 Via Mantova
3109 Honeysuckle Ave
3119 Blossom Glen Dr
3136 Alder Grove Ct
3145 E Flamingo Rd
3203 Lone Prarie Ct
3205 Honeysuckle Ave
3268 Cheyenne Gardens Way
3316 Jamaica Princess Pl
3318 N Decatur Blvd
3441 Mazzocco Ct
3508 Rio Robles Dr
3519 Clear Lake Ct
3529 Quiet Pueblo St
3626 Via Terracina
3634 Via Messina
3677 Steinbeck Dr
3684 Hidden Beach Ct
37 Delighted Ave
3750 State Rte 604
3777 Via Di Girolamo Ave
3837 Quail Creek Dr
39 W Main St
3903 Maple Creek Ave
3925 Counter Way
3936 Sheltering Pines St
396 Marston Way
""".strip().split(
    "\n"
)


def get_it(url):
    toc = default_timer()
    requests.get(url)
    return default_timer() - toc


class SpeedTests(TestCase):
    def test_speed(self):
        """make sure to run the server first"""
        urls = [f"http://localhost:8000/address/{item}" for item in address]
        with PoolExecutor(max_workers=4) as executor:
            times = []
            for timed in executor.map(get_it, urls):
                times.append(timed)
            print(sum(times) / len(times))

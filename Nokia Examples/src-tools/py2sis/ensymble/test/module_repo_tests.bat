set SDK_DRIVE=V:

python ensymble.py py2sis hello_world.py --extra-modules=app1 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp1.txt & zip test_results.zip temp1.txt & del temp1.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=app2 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp2.txt & zip test_results.zip temp2.txt & del temp2.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=app3 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp3.txt & zip test_results.zip temp3.txt & del temp3.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=app4 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp4.txt & zip test_results.zip temp4.txt & del temp4.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=app5 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp5.txt & zip test_results.zip temp5.txt & del temp5.txt hello_world_v1_0_0.sis

python ensymble.py py2sis my_app --extra-modules=app1 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp21.txt & zip test_results.zip temp21.txt & del temp21.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app2 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp22.txt & zip test_results.zip temp22.txt & del temp22.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app3 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp23.txt & zip test_results.zip temp23.txt & del temp23.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app4 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp24.txt & zip test_results.zip temp24.txt & del temp24.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app5 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp25.txt & zip test_results.zip temp25.txt & del temp25.txt my_app_v1_0_0.sis

python ensymble.py py2sis my_app --extra-modules=app1 --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp31.txt & zip test_results.zip temp31.txt & del temp31.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app2 --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp32.txt & zip test_results.zip temp32.txt & del temp32.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app3 --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp33.txt & zip test_results.zip temp33.txt & del temp33.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app4 --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp34.txt & zip test_results.zip temp34.txt & del temp34.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app5 --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp35.txt & zip test_results.zip temp35.txt & del temp35.txt my_app_v1_0_0.sis

python ensymble.py py2sis hello_world.py --extra-modules=os & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp41.txt & zip test_results.zip temp41.txt & del temp41.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=elemlist & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp42.txt & zip test_results.zip temp42.txt & del temp42.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=pickle & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp43.txt & zip test_results.zip temp43.txt & del temp43.txt hello_world_v1_0_0.sis

python ensymble.py py2sis my_app --extra-modules=os & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp51.txt & zip test_results.zip temp51.txt & del temp51.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=elemlist & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp52.txt & zip test_results.zip temp52.txt & del temp52.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp53.txt & zip test_results.zip temp53.txt & del temp53.txt my_app_v1_0_0.sis

python ensymble.py py2sis my_app --extra-modules=os --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp61.txt & zip test_results.zip temp61.txt & del temp61.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=elemlist --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp62.txt & zip test_results.zip temp62.txt & del temp62.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp63.txt & zip test_results.zip temp63.txt & del temp63.txt my_app_v1_0_0.sis

python ensymble.py py2sis hello_world.py --extra-modules=pickle.temp & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp71.txt & zip test_results.zip temp71.txt & del temp71.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=pickle.cpick & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp72.txt & zip test_results.zip temp72.txt & del temp72.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=pickle.cpick.rpo & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp73.txt & zip test_results.zip temp73.txt & del temp73.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=pickle.cpick.test & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp74.txt & zip test_results.zip temp74.txt & del temp74.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=pickle.cpick.test.test1 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp75.txt & zip test_results.zip temp75.txt & del temp75.txt hello_world_v1_0_0.sis

python ensymble.py py2sis my_app --extra-modules=pickle.temp & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp81.txt & zip test_results.zip temp81.txt & del temp81.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle.cpick & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp82.txt & zip test_results.zip temp82.txt & del temp82.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle.cpick.rpo & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp83.txt & zip test_results.zip temp83.txt & del temp83.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle.cpick.test & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp84.txt & zip test_results.zip temp84.txt & del temp84.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle.cpick.test.test1 & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp85.txt & zip test_results.zip temp85.txt & del temp85.txt my_app_v1_0_0.sis

python ensymble.py py2sis my_app --extra-modules=pickle.temp --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > temp91.txt & zip test_results.zip temp91.txt & del temp91.txt hello_world_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle.cpick --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp92.txt & zip test_results.zip temp92.txt & del temp92.txt hello_world_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle.cpick.rpo --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp93.txt & zip test_results.zip temp93.txt & del temp93.txt hello_world_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle.cpick.test --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp94.txt & zip test_results.zip temp94.txt & del temp94.txt hello_world_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=pickle.cpick.test.test1 --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > temp95.txt & zip test_results.zip temp95.txt & del temp95.txt hello_world_v1_0_0.sis

python ensymble.py py2sis hello_world.py --extra-modules=app2.test & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > tempA2.txt & zip test_results.zip tempA2.txt & del tempA2.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=app2.test.test & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > tempA3.txt & zip test_results.zip tempA3.txt & del tempA3.txt hello_world_v1_0_0.sis
python ensymble.py py2sis hello_world.py --extra-modules=app5.app2_mod & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l hello_world_v1_0_0.sis > tempA4.txt & zip test_results.zip tempA4.txt & del tempA4.txt hello_world_v1_0_0.sis

python ensymble.py py2sis my_app --extra-modules=app2.test & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > tempB2.txt & zip test_results.zip tempB2.txt & del tempB2.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app2.test.test & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > tempB3.txt & zip test_results.zip tempB3.txt & del tempB3.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app5.app2_mod & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > tempB4.txt & zip test_results.zip tempB4.txt & del tempB4.txt my_app_v1_0_0.sis

python ensymble.py py2sis my_app --extra-modules=app2.test --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > tempC2.txt & zip test_results.zip tempC2.txt & del tempC2.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app2.test.test --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > tempC3.txt & zip test_results.zip tempC3.txt & del tempC3.txt my_app_v1_0_0.sis
python ensymble.py py2sis my_app --extra-modules=app5.app2_mod --extrasdir=root & %SDK_DRIVE%\epoc32\tools\dumpsis.exe -l my_app_v1_0_0.sis > tempC4.txt & zip test_results.zip tempC4.txt & del tempC4.txt my_app_v1_0_0.sis

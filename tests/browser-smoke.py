from pathlib import Path
import json
import tempfile
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'app' / 'index.html'
HTML = APP.read_text()
MOCK_STORAGE = '''<script>(()=>{let store={};try{store=JSON.parse(window.name||'{}')}catch(e){};const save=()=>window.name=JSON.stringify(store);Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>Object.prototype.hasOwnProperty.call(store,k)?store[k]:null,setItem:(k,v)=>{store[k]=String(v);save()},removeItem:k=>{delete store[k];save()}}})})()</script>'''
def load_app(page): page.set_content(HTML.replace('<script>',MOCK_STORAGE+'<script>',1),wait_until='load')
results=[]
errors=[]
def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS' if ok else 'FAIL')+' | '+name+((' | '+detail) if detail else ''), flush=True)
    if not ok: raise AssertionError(f'{name}: {detail}')
def click_center(locator):
    locator.evaluate("el => { el.scrollIntoView({block:'center',behavior:'instant'}); el.click(); }")
def click_nav(locator):
    locator.evaluate('el => el.click()')

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox','--disable-dev-shm-usage'])
    context=browser.new_context(viewport={"width":390,"height":844}, accept_downloads=True)
    page=context.new_page(); page.set_default_timeout(4000)
    page.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page)
    page.wait_for_timeout(200)
    check('initial dashboard renders', page.locator('#heroTitle').inner_text() != '')
    check('dashboard uses active days rather than streak pressure', page.locator('#activeDaysCount').is_visible() and page.get_by_text('Active days this week').is_visible() and page.locator('#streakCount').count()==0)
    metric_page=context.new_page(); metric_page.set_default_timeout(4000); load_app(metric_page)
    metric_page.evaluate("""() => { const now=new Date(); const monday=new Date(now); monday.setHours(12,0,0,0); monday.setDate(monday.getDate()-((monday.getDay()+6)%7)); const future=new Date(now); future.setDate(future.getDate()+2); data.sessions=[{id:'week-a',date:monday.toISOString(),minutes:8,exercises:[],safetyStop:false},{id:'week-b',date:monday.toISOString(),minutes:7,exercises:[],safetyStop:false},{id:'future',date:future.toISOString(),minutes:99,exercises:[],safetyStop:false}]; updateUI(); }""")
    check('weekly dashboard counts distinct active days and excludes future-dated records', metric_page.locator('#weekCount').inner_text()=='2' and metric_page.locator('#activeDaysCount').inner_text()=='1' and metric_page.locator('#minuteCount').inner_text()=='15')
    check('all-time progress excludes future-dated sessions', metric_page.locator('#progressSessions').inner_text()=='2' and metric_page.locator('#progressMinutes').inner_text()=='15')
    metric_page.evaluate("""() => { data.sessions=[{id:'actual-completed',date:new Date().toISOString(),minutes:10,exercises:[],checkin:'manageable',safetyStop:false},{id:'future-safety',date:new Date(Date.now()+86400000*2).toISOString(),minutes:2,exercises:[],checkin:'pain',safetyStop:true}]; updateUI(); }""")
    check('future-dated safety stop does not override current teaching path', 'Repeat the current plan' in metric_page.locator('#pathNextAction').inner_text() or 'Repeat once more' in metric_page.locator('#pathNextAction').inner_text())
    metric_page.close()
    check('mobile layout shows bottom navigation without horizontal overflow', page.locator('.sidebar').is_hidden() and page.locator('.mobile-nav').is_visible() and page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
    desktop_context=browser.new_context(viewport={"width":1440,"height":900}); desktop=desktop_context.new_page(); desktop.set_default_timeout(4000); desktop.on('pageerror', lambda e: errors.append(str(e)))
    load_app(desktop)
    check('desktop layout shows sidebar and hides mobile navigation', desktop.locator('.sidebar').is_visible() and desktop.locator('.mobile-nav').is_hidden() and desktop.evaluate('document.documentElement.scrollWidth <= window.innerWidth'))
    check('active navigation is exposed to assistive technology', page.locator('[data-view="today"]').first.get_attribute('aria-current') == 'page' and page.locator('[data-view="workout"]').first.get_attribute('aria-current') is None)
    click_nav(page.locator('[data-view="path"]').last)
    check('teaching path has action and rationale', page.locator('#pathNextAction').inner_text() != '' and page.locator('#pathWhy').inner_text() != '')
    click_nav(page.locator('[data-view="settings"]').last)
    page.locator('#equipment').select_option('Bodyweight only')
    page.locator('#settingsForm button[type="submit"]').click()
    check('equipment preference updates plan', 'Chair squat' in page.locator('#todayExercises').inner_text())
    click_nav(page.locator('[data-view="workout"]').last)
    page.wait_for_timeout(250)
    page.evaluate("resetPlayer();document.querySelector('#playerSetup').scrollIntoView({block:'start',behavior:'instant'})")
    check('reset clears selected difficulty state for the next session', all(page.locator('#checkin'+v).get_attribute('aria-pressed')=='false' for v in ['Easy','Manageable','Hard']))
    click_center(page.get_by_role('button', name='Begin session'))
    check('session player starts', page.locator('#playerActive').is_visible())
    page.locator('#pauseBtn').click()
    check('timer pause control responds', page.locator('#sessionState').inner_text() == 'PAUSED' and page.locator('#pauseBtn').get_attribute('aria-pressed') == 'true')
    page.locator('#pauseBtn').click()
    check('resume control exposes unpressed state', page.locator('#pauseBtn').get_attribute('aria-pressed') == 'false')
    page.evaluate("timerEndsAt=Date.now()-100;document.dispatchEvent(new Event('visibilitychange'))")
    check('timer catches up from elapsed wall-clock time', page.locator('#sessionState').inner_text() == 'TIME COMPLETE')
    for _ in range(4):
        if page.locator('#playerDone').is_visible(): break
        page.locator('#completeBtn').click()
    check('workout reaches check-in', page.locator('#playerDone').is_visible())
    click_center(page.locator('#saveSessionBtn'))
    check('completed workout requires check-in', page.locator('#playerDone').is_visible() and 'Choose Easier' in page.locator('#sessionCheckinHelp').inner_text())
    page.locator('#checkinManageable').click()
    check('difficulty check-in exposes the selected choice to assistive technology', page.locator('#checkinManageable').get_attribute('aria-pressed')=='true' and page.locator('#checkinEasy').get_attribute('aria-pressed')=='false')
    click_center(page.locator('#saveSessionBtn'))
    stored=page.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('check-in saved on exact session', len(stored['sessions']) == 1 and stored['sessions'][0]['checkin'] == 'manageable' and stored['pathFeedback'][0]['sessionId'] == stored['sessions'][0]['id'])
    click_nav(page.locator('[data-view="workout"]').last)
    page.wait_for_timeout(250)
    page.evaluate("resetPlayer();document.querySelector('#playerSetup').scrollIntoView({block:'start',behavior:'instant'})")
    click_center(page.get_by_role('button', name='Begin session'))
    page.get_by_role('button', name='Pain or unsafe movement').click()
    check('pain report disables exercise actions', page.locator('#completeBtn').is_disabled() and page.locator('#skipBtn').is_disabled())
    click_center(page.get_by_role('button', name='End and record safety stop'))
    check('safety stop uses separate save flow', page.locator('#doneEyebrow').inner_text() == 'SESSION STOPPED FOR SAFETY')
    click_center(page.locator('#saveSessionBtn'))
    stored=page.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('safety stop is logged but excluded from completed-workout totals', stored['sessions'][0]['safetyStop'] is True and page.locator('#progressSessions').inner_text() == '1')
    page.evaluate("showView('path')")
    check('safety stop prevents path progression', 'Safety comes before progression' in page.locator('#pathWhy').inner_text() and 'Stage 2 of 3' in page.locator('#stagePill').inner_text())
    page.get_by_role('button', name='Manageable').dispatch_event('click')
    stored=page.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('safety report cannot be overwritten as manageable', stored['sessions'][0]['checkin'] == 'pain')
    storage_snapshot=page.evaluate('window.name')
    page2=context.new_page(); page2.set_default_timeout(4000); page2.on('pageerror', lambda e: errors.append(str(e)))
    page2.evaluate('(v)=>window.name=v',storage_snapshot)
    load_app(page2)
    page=page2
    stored=page.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('history persists across a fresh page load', len(stored['sessions']) == 2)
    page.evaluate("showView('settings')")
    page.on('dialog', lambda dialog: dialog.accept())
    page.evaluate("['lifeAppPrototype07','lifeAppPrototype06','lifeAppPrototype05','lifeAppPrototype04','lifeAppPrototype02'].forEach(k=>localStorage.setItem(k,'legacy-test-data'))")
    page.locator('button.danger').last.click(force=True)
    check('clear data removes current and all supported migration keys', all(page.evaluate("k=>localStorage.getItem(k)", k) is None for k in ['lifeAppPrototype15','lifeAppPrototype14','lifeAppPrototype13','lifeAppPrototype12','lifeAppPrototype11','lifeAppPrototype10','lifeAppPrototype09','lifeAppPrototype08','lifeAppPrototype07','lifeAppPrototype06','lifeAppPrototype05','lifeAppPrototype04','lifeAppPrototype02']))

    # A path-review check-in should influence the recommendation without rewriting
    # the original post-session check-in stored on the workout itself.
    page3=context.new_page(); page3.set_default_timeout(4000); page3.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page3)
    page3.evaluate("""() => { const now=new Date().toISOString(); data.sessions=[{id:'s1',date:now,minutes:8,exercises:['Chair squat'],reflection:'',goal:'Build strength',checkin:'easy',safetyStop:false,outcome:'completed'}]; data.pathFeedback=[{sessionId:'s1',value:'easy',date:now,source:'session-checkin'}]; persist(); updateUI(); showView('path'); }""")
    page3.get_by_role('button', name='Too difficult').click()
    stored=page3.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('path review does not rewrite original session feedback', stored['sessions'][0]['checkin']=='easy' and stored['pathFeedback'][0]['value']=='hard')
    check('path review updates next-step teaching', 'shorter session' in page3.locator('#pathNextAction').inner_text())

    # Stage 3 requires three completed sessions and two recent manageable/easy
    # check-ins; a safety stop must never count as one of those sessions.
    page4=context.new_page(); page4.set_default_timeout(4000); page4.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page4)
    page4.evaluate("""() => { const now=Date.now(); data.sessions=[0,1,2].map((n)=>({id:'stage'+n,date:new Date(now-n*86400000).toISOString(),minutes:10,exercises:['Chair squat'],reflection:'',goal:'Build strength',checkin:n<2?'manageable':'hard',safetyStop:false,outcome:'completed'})); data.pathFeedback=[]; persist(); updateUI(); showView('path'); }""")
    check('repeated manageable sessions can reach gradual progression stage', page4.locator('#stagePill').inner_text()=='Stage 3 of 3')
    page4.evaluate("""() => { data.sessions.unshift({id:'safe',date:new Date().toISOString(),minutes:1,exercises:[],reflection:'',goal:'Build strength',checkin:'pain',safetyStop:true,outcome:'stopped'}); persist(); updateUI(); showView('path'); }""")
    check('new safety stop takes precedence over progression stage', 'Safety comes before progression' in page4.locator('#pathWhy').inner_text())

    # Verify migration from a supported older key to the current key.
    page5=context.new_page(); page5.set_default_timeout(4000); page5.on('pageerror', lambda e: errors.append(str(e)))
    page5.evaluate("""() => { window.name=JSON.stringify({lifeAppPrototype05:JSON.stringify({prefs:{name:'Legacy',goal:'Build strength',equipment:'Bodyweight only',duration:'10',level:'Beginner / getting back into it'},sessions:[{id:'old',date:new Date().toISOString(),minutes:5,exercises:[],checkin:'manageable',safetyStop:false}],pathFeedback:[]})}); }""")
    load_app(page5)
    migrated=page5.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('Prototype 0.5 data migrates to current storage key', migrated['prefs']['name']=='Legacy' and migrated['sessions'][0]['id']=='old')

    # The Prototype 0.7 build used the 0.6 key. Verify the version bump migrates
    # that legacy key to 0.8 without dropping session history.
    page6=context.new_page(); page6.set_default_timeout(4000); page6.on('pageerror', lambda e: errors.append(str(e)))
    page6.evaluate("""() => { window.name=JSON.stringify({lifeAppPrototype06:JSON.stringify({prefs:{name:'Prototype 0.6',goal:'Build strength',equipment:'Dumbbells and bodyweight',duration:'12',level:'Beginner / getting back into it'},sessions:[{id:'v06',date:new Date().toISOString(),minutes:7,exercises:[],checkin:'manageable',safetyStop:false}],pathFeedback:[]})}); }""")
    load_app(page6)
    migrated06=page6.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('Prototype 0.6 data migrates to 1.5 without losing session history', migrated06['prefs']['name']=='Prototype 0.6' and migrated06['sessions'][0]['id']=='v06' and page6.evaluate("localStorage.getItem('lifeAppPrototype06')") is not None)

    page08=context.new_page(); page08.set_default_timeout(4000); page08.on('pageerror', lambda e: errors.append(str(e)))
    page08.evaluate("() => { window.name=JSON.stringify({lifeAppPrototype08:JSON.stringify({prefs:{name:'Prototype 0.8',goal:'Build strength',equipment:'Bodyweight only',duration:'10',level:'Beginner / getting back into it'},sessions:[{id:'v08',date:new Date().toISOString(),minutes:8,exercises:[],checkin:'manageable',safetyStop:false}],pathFeedback:[]})}); }")
    load_app(page08)
    migrated08=page08.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('Prototype 0.8 data migrates to 1.5 without losing history', migrated08['prefs']['name']=='Prototype 0.8' and migrated08['sessions'][0]['id']=='v08' and page08.evaluate("localStorage.getItem('lifeAppPrototype08')") is not None)

    page09=context.new_page(); page09.set_default_timeout(4000); page09.on('pageerror', lambda e: errors.append(str(e)))
    page09.evaluate("() => { window.name=JSON.stringify({lifeAppPrototype09:JSON.stringify({prefs:{name:'Prototype 0.9',goal:'Build strength',equipment:'Bodyweight only',duration:'10',level:'Beginner / getting back into it'},sessions:[{id:'v09',date:new Date().toISOString(),minutes:9,exercises:[],checkin:'manageable',safetyStop:false}],pathFeedback:[]})}); }")
    load_app(page09)
    migrated09=page09.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('Prototype 0.9 data migrates to 1.5 without losing history', migrated09['prefs']['name']=='Prototype 0.9' and migrated09['sessions'][0]['id']=='v09' and page09.evaluate("localStorage.getItem('lifeAppPrototype09')") is not None)

    # Prototype 1.1 data should migrate to the new 1.2 storage key without loss.
    page11=context.new_page(); page11.set_default_timeout(4000); page11.on('pageerror', lambda e: errors.append(str(e)))
    page11.evaluate("""() => { window.name=JSON.stringify({lifeAppPrototype11:JSON.stringify({prefs:{name:'Prototype 1.1',goal:'Build strength',equipment:'Bodyweight only',duration:'10',level:'Beginner / getting back into it'},sessions:[{id:'v11',date:new Date().toISOString(),minutes:11,exercises:['Chair squat'],checkin:'manageable',safetyStop:false,outcome:'completed'}],pathFeedback:[]})}); }""")
    load_app(page11)
    migrated11=page11.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('Prototype 1.1 data migrates to 1.5 without losing session history', migrated11['prefs']['name']=='Prototype 1.1' and migrated11['sessions'][0]['id']=='v11' and page11.evaluate("localStorage.getItem('lifeAppPrototype11')") is not None)

    # Prototype 1.0 data should migrate to the new 1.2 storage key without loss.
    page10=context.new_page(); page10.set_default_timeout(4000); page10.on('pageerror', lambda e: errors.append(str(e)))
    page10.evaluate("""() => { window.name=JSON.stringify({lifeAppPrototype10:JSON.stringify({prefs:{name:'Prototype 1.0',goal:'Build strength',equipment:'Bodyweight only',duration:'10',level:'Beginner / getting back into it'},sessions:[{id:'v10',date:new Date().toISOString(),minutes:10,exercises:['Chair squat'],checkin:'manageable',safetyStop:false,outcome:'completed'}],pathFeedback:[]})}); }""")
    load_app(page10)
    migrated10=page10.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('Prototype 1.0 data migrates to 1.5 without losing session history', migrated10['prefs']['name']=='Prototype 1.0' and migrated10['sessions'][0]['id']=='v10' and page10.evaluate("localStorage.getItem('lifeAppPrototype10')") is not None)

    # Prototype 1.2 data should migrate through supported keys to current 1.5 without loss.
    page12=context.new_page(); page12.set_default_timeout(4000); page12.on('pageerror', lambda e: errors.append(str(e)))
    page12.evaluate("""() => { window.name=JSON.stringify({lifeAppPrototype12:JSON.stringify({prefs:{name:'Prototype 1.2',goal:'Build strength',equipment:'Bodyweight only',duration:'10',level:'Beginner / getting back into it'},sessions:[{id:'v12',date:new Date().toISOString(),minutes:12,exercises:['Chair squat'],checkin:'manageable',safetyStop:false,outcome:'completed'}],pathFeedback:[]})}); }""")
    load_app(page12)
    migrated12=page12.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('Prototype 1.2 data migrates to 1.5 without losing session history', migrated12['prefs']['name']=='Prototype 1.2' and migrated12['sessions'][0]['id']=='v12' and page12.evaluate("localStorage.getItem('lifeAppPrototype12')") is not None)

    # Export should download a readable backup without mutating app storage.
    page6.evaluate("() => { data.prefs.name='Export test'; data.sessions=[{id:'export-session',date:new Date().toISOString(),minutes:9,exercises:['Chair squat'],reflection:'test note',goal:'Build strength',checkin:'manageable',safetyStop:false,outcome:'completed'}]; data.pathFeedback=[{sessionId:'export-session',value:'manageable',date:new Date().toISOString()}]; persist(); fillSettings(); showView('settings'); }")
    # Prototype 1.4 data should migrate to 1.5 without deleting the source key.
    page13=context.new_page(); page13.set_default_timeout(4000); page13.on('pageerror', lambda e: errors.append(str(e)))
    page13.evaluate("""() => { window.name=JSON.stringify({lifeAppPrototype14:JSON.stringify({prefs:{name:'Prototype 1.4',goal:'Build strength',equipment:'Bodyweight only',duration:'10',level:'Beginner / getting back into it'},sessions:[{id:'v14',date:new Date().toISOString(),minutes:12,exercises:['Chair squat'],checkin:'manageable',safetyStop:false,outcome:'completed'}],pathFeedback:[]})}); }""")
    load_app(page13)
    migrated13=page13.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('Prototype 1.4 data migrates to 1.5 without losing session history', migrated13['prefs']['name']=='Prototype 1.4' and migrated13['sessions'][0]['id']=='v14' and page13.evaluate("localStorage.getItem('lifeAppPrototype14')") is not None)

    # Accessibility smoke checks: skip link, visible keyboard focus, reduced motion,
    # progress semantics and selected difficulty state.
    check('keyboard skip link targets main content', page.locator('.skip-link').get_attribute('href')=='#mainContent' and page.locator('#mainContent').get_attribute('tabindex')=='-1')
    page.locator('.skip-link').focus()
    check('skip link becomes visible on keyboard focus', page.locator('.skip-link').evaluate("el => getComputedStyle(el).transform === 'matrix(1, 0, 0, 1, 0, 0)'"))
    page.emulate_media(reduced_motion='reduce')
    check('reduced-motion preference minimizes transitions', page.locator('button').first.evaluate("el => parseFloat(getComputedStyle(el).transitionDuration) <= 0.001"))
    check('weekly target exposes accessible progress semantics', page.locator('#weekProgress').get_attribute('role')=='progressbar' and page.locator('#weekProgress').get_attribute('aria-valuemax')=='3')
    check('basic accessible-name audit finds named buttons and form fields with one page H1', page.evaluate("() => [...document.querySelectorAll('button')].every(e => ((e.innerText||'').trim() || e.getAttribute('aria-label') || e.getAttribute('aria-labelledby') || e.title)) && [...document.querySelectorAll('input:not([type=hidden]),select,textarea')].every(e => (e.labels&&e.labels.length) || e.getAttribute('aria-label') || e.getAttribute('aria-labelledby')) && document.querySelectorAll('h1').length===1"))
    page.emulate_media(reduced_motion='no-preference')

    before_export=page6.evaluate("localStorage.getItem('lifeAppPrototype15')")
    with page6.expect_download() as download_info:
        page6.get_by_role('button', name='Export my data').click()
    download=download_info.value
    exported=json.loads(Path(download.path()).read_text())
    check('data export downloads valid JSON with preferences, history and path feedback', exported['appVersion']=='1.5' and exported['schemaVersion']==1 and exported['data']['prefs']['name']=='Export test' and exported['data']['sessions'][0]['id']=='export-session' and exported['data']['pathFeedback'][0]['sessionId']=='export-session' and download.suggested_filename.startswith('life-app-backup-'))
    check('export contains only the documented app metadata and data sections', set(exported.keys())=={'app','appVersion','schemaVersion','exportedAt','data'} and set(exported['data'].keys())=={'prefs','sessions','pathFeedback'})
    check('export leaves the saved app data unchanged', page6.evaluate("localStorage.getItem('lifeAppPrototype15')") == before_export)

    # Restore must validate a complete backup and ask before replacing current data.
    page7=context.new_page(); page7.set_default_timeout(4000); page7.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page7)
    page7.evaluate("() => { data.prefs.name='Current data'; data.sessions=[{id:'keep',date:new Date().toISOString(),minutes:3,exercises:['Chair squat'],reflection:'Keep this until restore',goal:'Build strength',checkin:'manageable',safetyStop:false,outcome:'completed'}]; data.pathFeedback=[]; persist(); updateUI(); showView('settings'); }")
    valid_backup={'app':'Life App','appVersion':'1.5','schemaVersion':1,'exportedAt':'2026-10-16T00:00:00.000Z','data':{'prefs':{'name':'Restored user','goal':'Build routine','equipment':'Bodyweight only','duration':'10','level':'Beginner / getting back into it'},'sessions':[{'id':'restored-1','date':'2026-10-15T12:00:00.000Z','minutes':9,'exercises':['Chair squat','Wall push-up'],'reflection':'Restored history','goal':'Build a routine','checkin':'manageable','safetyStop':False,'outcome':'completed','unexpectedField':'must not persist'}, {'id':'restored-safety','date':'2026-10-16T12:00:00.000Z','minutes':4,'exercises':['Chair squat'],'reflection':'Safety report','goal':'Build strength','checkin':'pain','safetyStop':False,'outcome':'completed'}],'pathFeedback':[{'sessionId':'restored-1','value':'manageable','date':'2026-10-15T12:00:00.000Z'}]}}
    with tempfile.NamedTemporaryFile('w',suffix='.json',encoding='utf-8',delete=False) as f:
        json.dump(valid_backup,f); valid_backup_path=f.name
    page7.on('dialog', lambda dialog: dialog.accept())
    page7.locator('#importFile').set_input_files(valid_backup_path)
    page7.wait_for_function("JSON.parse(localStorage.getItem('lifeAppPrototype15')||'{}').prefs?.name==='Restored user'")
    restored=page7.evaluate("JSON.parse(localStorage.getItem('lifeAppPrototype15'))")
    check('valid backup restore replaces preferences and restores linked history', restored['prefs']['name']=='Restored user' and restored['sessions'][1]['id']=='restored-1' and restored['pathFeedback'][0]['sessionId']=='restored-1' and page7.locator('#equipment').input_value()=='Bodyweight only')
    check('restore strips unknown fields and never downgrades a pain report', 'unexpectedField' not in restored['sessions'][1] and restored['sessions'][0]['safetyStop'] is True and restored['sessions'][0]['outcome']=='stopped')
    check('restored history is sorted newest-first by session date', restored['sessions'][0]['id']=='restored-safety' and restored['sessions'][1]['id']=='restored-1')
    page7.evaluate("() => { updateUI(); showView('path'); }")
    check('newest restored safety stop takes precedence over older completed session', 'Safety comes before progression' in page7.locator('#pathWhy').inner_text())

    page8=context.new_page(); page8.set_default_timeout(4000); page8.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page8)
    page8.evaluate("() => { data.prefs.name='Keep current'; data.sessions=[{id:'safe-current',date:new Date().toISOString(),minutes:2,exercises:['Chair squat'],reflection:'Current',goal:'Build strength',checkin:'easy',safetyStop:false,outcome:'completed'}]; data.pathFeedback=[]; persist(); showView('settings'); }")
    before_invalid=page8.evaluate("localStorage.getItem('lifeAppPrototype15')")
    with tempfile.NamedTemporaryFile('w',suffix='.json',encoding='utf-8',delete=False) as f:
        f.write('{not valid json'); invalid_backup_path=f.name
    page8.locator('#importFile').set_input_files(invalid_backup_path)
    page8.get_by_text('That file is not valid JSON. Your current data was not changed.').wait_for()
    check('invalid backup is rejected without changing existing data', page8.evaluate("localStorage.getItem('lifeAppPrototype15')") == before_invalid)

    # Reject duplicate session IDs and oversized history before confirmation or mutation.
    page_dup=context.new_page(); page_dup.set_default_timeout(4000); page_dup.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page_dup)
    page_dup.evaluate("() => { data.prefs.name='Keep duplicate test'; data.sessions=[]; data.pathFeedback=[]; persist(); showView('settings'); }")
    before_dup=page_dup.evaluate("localStorage.getItem('lifeAppPrototype15')")
    duplicate_backup={**valid_backup,'data':{**valid_backup['data'],'sessions':[dict(valid_backup['data']['sessions'][0],id='duplicate'),dict(valid_backup['data']['sessions'][1],id='duplicate')]}}
    with tempfile.NamedTemporaryFile('w',suffix='.json',encoding='utf-8',delete=False) as f:
        json.dump(duplicate_backup,f); duplicate_backup_path=f.name
    page_dup.locator('#importFile').set_input_files(duplicate_backup_path)
    page_dup.get_by_text('This backup contains duplicate session IDs. Your current data was not changed.').wait_for()
    check('duplicate session IDs are rejected without changing current data', page_dup.evaluate("localStorage.getItem('lifeAppPrototype15')") == before_dup)

    page_large=context.new_page(); page_large.set_default_timeout(4000); page_large.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page_large)
    page_large.evaluate("() => { data.prefs.name='Keep large test'; data.sessions=[]; data.pathFeedback=[]; persist(); showView('settings'); }")
    before_large=page_large.evaluate("localStorage.getItem('lifeAppPrototype15')")
    large_backup={**valid_backup,'data':{**valid_backup['data'],'sessions':[dict(valid_backup['data']['sessions'][0],id=f'bulk-{i}') for i in range(5001)]}}
    with tempfile.NamedTemporaryFile('w',suffix='.json',encoding='utf-8',delete=False) as f:
        json.dump(large_backup,f); large_backup_path=f.name
    page_large.locator('#importFile').set_input_files(large_backup_path)
    page_large.get_by_text('This backup contains too many sessions to restore safely. Your current data was not changed.').wait_for()
    check('oversized session history is rejected without changing current data', page_large.evaluate("localStorage.getItem('lifeAppPrototype15')") == before_large)

    page_feedback=context.new_page(); page_feedback.set_default_timeout(4000); page_feedback.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page_feedback)
    page_feedback.evaluate("() => { data.prefs.name='Keep feedback test'; data.sessions=[]; data.pathFeedback=[]; persist(); showView('settings'); }")
    before_feedback=page_feedback.evaluate("localStorage.getItem('lifeAppPrototype15')")
    feedback_backup={**valid_backup,'data':{**valid_backup['data'],'sessions':[],'pathFeedback':[{'sessionId':None,'value':'manageable','date':'2026-10-15T12:00:00.000Z'} for _ in range(1001)]}}
    with tempfile.NamedTemporaryFile('w',suffix='.json',encoding='utf-8',delete=False) as f:
        json.dump(feedback_backup,f); feedback_backup_path=f.name
    page_feedback.locator('#importFile').set_input_files(feedback_backup_path)
    page_feedback.get_by_text('This backup contains too many feedback records to restore safely. Your current data was not changed.').wait_for()
    check('oversized feedback history is rejected without changing current data', page_feedback.evaluate("localStorage.getItem('lifeAppPrototype15')") == before_feedback)

    page9=context.new_page(); page9.set_default_timeout(4000); page9.on('pageerror', lambda e: errors.append(str(e)))
    load_app(page9)
    page9.evaluate("() => { data.prefs.name='Keep after cancel'; data.sessions=[]; data.pathFeedback=[]; persist(); showView('settings'); }")
    before_cancel=page9.evaluate("localStorage.getItem('lifeAppPrototype15')")
    page9.on('dialog', lambda dialog: dialog.dismiss())
    page9.locator('#importFile').set_input_files(valid_backup_path)
    page9.wait_for_timeout(100)
    check('cancelled restore leaves existing data unchanged', page9.evaluate("localStorage.getItem('lifeAppPrototype15')") == before_cancel)


    # Simulate browser storage quota/security failure and ensure the UI does not claim success.
    storage_fail=context.new_page(); storage_fail.set_default_timeout(4000); storage_fail.on('pageerror', lambda e: errors.append(str(e)))
    load_app(storage_fail)
    storage_fail.evaluate("() => { window.__originalSetItem=localStorage.setItem.bind(localStorage); localStorage.setItem=()=>{throw new DOMException('Quota exceeded','QuotaExceededError')}; showView('settings'); }")
    storage_fail.locator('#name').fill('Unsaved test')
    storage_fail.locator('#settingsForm button[type=submit]').click()
    check('storage write failure shows a clear warning instead of a false save confirmation', 'Could not save to this device' in storage_fail.locator('#toast').inner_text() and storage_fail.locator('#view-settings').is_visible())
    storage_fail.evaluate("() => { localStorage.setItem=window.__originalSetItem; }")
    storage_fail.close()

    check('no browser JavaScript errors', not errors, '; '.join(errors))
    desktop_context.close()
    browser.close()

for fixture in (locals().get('valid_backup_path'), locals().get('invalid_backup_path'), locals().get('duplicate_backup_path'), locals().get('large_backup_path'), locals().get('feedback_backup_path')):
    if fixture and Path(fixture).exists(): Path(fixture).unlink()

print(f'RESULT: {sum(ok for _,ok,_ in results)}/{len(results)} checks passed')

source venv/bin/activate

pip install -e miroblock
python xblock-sdk/manage.py runserver

stdudent view
localhost:8000/scenario/miroblock.0/

studio view
localhost:8000/scenario/miroblock.0/studio_view


https://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html#installing-the-xblock
https://blog.twshop.asia/在openedx自訂一個xblock組件/
https://edx.readthedocs.io/projects/edx-developer-guide/en/latest/extending_platform/xblocks.html#lms
http://gitlab.dlc.ntu.edu.tw/open-edx/edx-platform/-/wikis/XBlock-%E9%96%8B%E7%99%BC%E6%B5%81%E7%A8%8B?version_id=42c025652cc68664fc8759126ece337d89d7927e



deploy:
lms> envs>devstack.py

LOGIN_REDIRECT_WHITELIST.extend([
    CMS_BASE,
    'localhost:2001',
])
MIRO_MICROFRONTEND_URL= 'http://localhost:2020'

lms/admin
Change site configuration
{
    "COURSE_CATALOG_API_URL": "http://edx.devstack.discovery:18381/api/v1/"
}




https://github.com/edx/edx-platform/blob/master/lms/djangoapps/grades/signals/handlers.py
   
  self.runtime.publish(self, "grade", { 
                        "value": submission_result,
                        "max_value": 1.0 })
   傳回，些事件似乎是決定一個課程是否通過                      
   COURSE_GRADE_NOW_FAILED

   要給分數應用



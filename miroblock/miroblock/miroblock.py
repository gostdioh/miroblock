"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
import requests

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, String, Scope
from submissions import api as submissions_api

@XBlock.needs("user")
class MiroXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    has_score = True
    
    bearer = String(
        default="", scope=Scope.settings,
        help="Bearer token",
    )

    boardid = String(
        default="", scope=Scope.settings,
        help="Board ID",       
    )

    viewLink = String(
        default="", scope=Scope.settings,
        help="View Link",       
    )


    boardId = String(
        default="", scope=Scope.settings,
        help="Board ID",       
    )
    # ------- External, Editable Fields -------
    display_name = String(
        display_name="Display Name", 
        default="建立miro白板",
        scope=Scope.settings,
        help="Name of this XBlock" 
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio. （設定用，preview 為author_view 
        """
        html_str = self.resource_string( "static/html/miroblock_edit.html")
        
        bearer = self.bearer or ''
        frag = Fragment(html_str.format(bearer=bearer ))
        frag.add_css(self.resource_string("static/css/miroblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/miroblock_edit.js"))
        frag.initialize_js('MiroXBlockEdit')
        return frag
    
    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        try:
            user_service = self.runtime.service(self, 'user')
            user = user_service.get_current_user()
            username = user.opt_attrs.get('edx-platform.username')
            print(data.get('bearer'))
            self.bearer = data.get('bearer')
            response={'result': 'success'}
            
        except Exception as e:
            log.exception(e)
            response = {
                'success': False,
                'error': str(e)
            }

        return response
    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the MiroXBlock, shown to students
        when viewing courses.
        """
        bearer = self.bearer or ''
        viewLink=self.viewLink or ''
        html = self.resource_string("static/html/miroblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/miroblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/miroblock.js"))
        frag.initialize_js('MiroXBlock')
        return frag

    
    
    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def upload_contribution(self, data, suffix=''):
        try:
            user_service = self.runtime.service(self, 'user')
            user = user_service.get_current_user()
            user_id = user.opt_attrs.get('edx-platform.user_id')
            username = user.opt_attrs.get('edx-platform.username')
            url = "https://api.miro.com/v1/boards/"+self.boardId+"/widgets/"
            print(url)
            headers = {
                "Accept": "application/json",
            "Authorization": "Bearer "+ self.bearer
            }
            
            print(headers)
            response = requests.request("GET", url, headers=headers)
            print(response)
            resData = response.json()
            ncount=resData['size']
            submission_result =0
            for x in range(ncount):
                widget=resData['data'][x]
                cname=widget['createdBy']['name']
                if cname ==username:
                    submission_result=submission_result+1

                mname =widget['modifiedBy']['name']
                if mname ==username:
                    submission_result=submission_result+1

                print(cname)
                print(mname)
            submission_result= submission_result/(ncount*2)+0.1
            # answer = {}
            # print( data)
            # print("data + scope_ids ")
            # print(self.scope_ids)
            # student_id = str(self.scope_ids.user_id)
            # item_id = str(self.scope_ids.usage_id)
            # course_id=str(self.scope_ids.usage_id.course_key)

            # student_item =dict(
            #     student_id=user_id,
            #     item_id=item_id,
            #     course_id=course_id,
            #     item_type='miroblock'
            #         ) ## xblock.get_student_item_dict()
            # submission = submissions_api.create_submission(student_item, answer)
            # print(submission)
            
            # submissions_api.set_score(submission["uuid"], 5, 10)
            
            print("set score")
            self.runtime.publish(self, "grade", { 
                        "value": submission_result,
                        "max_value": 1.0 
                        })
            
            print(username)
            ret ={'result': 'success',
                  'success': True}
        except Exception as e:
            print(e)
            ret = {
                'success': False,
                'error': str(e)
            }
        return ret

        

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def add_board(self, data, suffix=''):
        print("add_board called")
        ret ="請先存access token"
        print(self.bearer)

        if  not self.bearer=="" :
            print(self.bearer )
            url = "https://api.miro.com/v1/boards"

            payload = {
                "name": "Untitled",
                "sharingPolicy": {
                    "access": "private",
                    "teamAccess": "private"
                }
            }
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.bearer
            }
            response = requests.request("POST", url, json=payload, headers=headers)
            resData = response.json()
            print(resData)
            self.viewLink =resData['viewLink'].replace('board','live-embed')
            self.boardId = resData['id']
            print(self.boardId)
            ret = "新白板建立"
        # Just to show data coming in...
        #assert data['hello'] == 'world'
        print("returned")
        return {"result": ret}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MiroXBlock",
             """<miroblock/>
             """),
            ("Multiple MiroXBlock",
             """<vertical_demo>
                <miroblock/>
                <miroblock/>
                <miroblock/>
                </vertical_demo>
             """),
        ]

## 주다, TEST
---

#### Command
    1. Open zshrc or bashrc
    
    2. Add below command and save
    alias test-jooda="cd repo && python3 manage.py test && rm -rf churchs/ && cd .."
    
    3. Apply zshrc or bashrc
    source ~/.zshrc or source ~/.bashrc

    4. Run Test
    [path : api.jooda.com]
    jooda-test
#### Unit Test

    Root Test Case
    
    🫥 JoodaTestCase 🫥
    # repo/common/test/test_case/test_case.py

> **Basic Behavior**
> > settings.TEST = True
> 
> **Object Variable**
> > client
> > image
> 
> **Method**
> > **API_Method**
> > > url = self.api_url<br>
> > > headers = self.headers<br>
> > > api_get<br>
> > > api_post<br>
> > > api_patch<br>
> >
> > **get_content_from_response**
> > > return response content data<br>
> > > api call success : return payload<br>
> > > api call failed : return error_code<br>
> >
> > **assertValidatePayload**
> > > if api call success, compare payload data to serializer field<br>
> > > if differnt two datas, test failed<br>

    Usage
    - JoodaTestCase 상속해서 앱 단위 테스트 케이스 생성
    # repo/common/test/test_case/{app_name}_test_case.py


    class {app_name}TestCase(JoodaTestCase):
    api_url = f"/{enums.ApiUrl.V1}{app_name}/"

    def setUp(self) -> None:
        self.headers = {"HTTP_Authorization": {header}}
        return super().setUp()



    - 실제 unit 테스트 파일에서 {app_name}TestCase 상속 받아서 사용

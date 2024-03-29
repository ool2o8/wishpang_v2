
## 1. 프로젝트 개요
### 👧 인력구성
  + 개인 프로젝트
### 🪄 프로젝트 목적
  + 쿠팡 상품의 경우 매일 상품의 가격이 달라지는데 상품 구매 직후 가격이 인하하여 안타까운 경험이 있다.
    가격 변동 추이를 파악하여 구매하려는 상품의 시세를 보여파악하고 구매시기 결정에 도움을 준다. <br>
### ⚙️ 환경
   + ``` python3.10 ```
   + **Framework** :Fastapi (기존 Django)
   + **Database** : Postgresql
   + **OS** : unix(mac) | EC2 - linux(Ubunut22.04)

## 3. 개발일지 🗓📆
#### v1.
* 2022.06.26 개발환경 셋팅, 장고 앱 생성
* 2022.07.04 DRF-JWT를 이용한 로그인 구현 중 (추후 django4 에서 jwt를 지원하지 않아 세션로그인으로 변경) 
* 2022.07.05 kakao login api 연결 (account\login view 작성)
* 2022.07.06 kakao login 유저 정보 불러오기->회원가입에 이용
* 2022.07.07 User 모델 확장- OneToOne profile 모델 생성, 비밀번호 해싱, 패키징 관리
* 2022.07.08 ~ 9 session authentication으로 로그인, 
* 2022.07.26 Wishpang 프로젝트 - 쿠팡 장바구니 상품 가격비교, 백그라운드 함수 호출 구현 중
permmition class 지정  permmition class 지정
* 2022-07-27 상품 가격 비교 뷰 작성 -ing
* 2022-07-28 상품 최저가 필터링
* 2022-07-31 aws rds 데이터 베이스 연결
* 2022-09. rds, ec2 연결 해제
* 2022-12. 상품정보 리팩토링

#### v2. 
* 2024.01.14 개발환경 세팅 (도커), 초기 앱 생성, 데이터베이스 연결
* 2024.01.15 카카오 로그인, 유저 생성 기능
 
## 4. 기능
  + **회원가입**<br>
    User 모델의 objects.create_user기능을 이용하여 유효성 검사와 저장을 한번에 수행합니다. <br>
  + **로그인 & 로그아웃**<br>
    + **로그인 시퀀스 다이어그램**<br>
      <img src=https://user-images.githubusercontent.com/59391473/203673983-2c1ab92b-7674-45dd-9426-b025b2b1d46a.png width="500" height="400"/><br>
      <br>
    + **코드**
    
    ```python
    class loginView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def create(self, request):
        serializer = UserSerializer(request.POST)
        user = authenticate(request, username=request.POST.get(       //django.contrib.auth의 `authenticate`을 이용하여 신원을 확인하고 반환
            'username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)                                      //반환된 유저가 있다면 `login()` 함수를 통해 세션 테이블에 저장하고 로그인 유지
            return redirect("http://127.0.0.1/blog/post")
        else:
            return redirect("http://127.0.0.1/account/register")
     ```
    + 'django.contrib.auth'의 'logout'를 이용해 세션 데이터를 삭제하고 로그아웃할 수 있습니다.
    + **카카오 로그인 시퀀스 다이어그램**<br>
    <img src=https://user-images.githubusercontent.com/59391473/204266712-ef926729-d63e-4970-b818-6d6044b1ebe1.png width="550" height="400"/><br>
      
      + 접근 권한 관리<br>
        Permission을 커스텀하여 회원과 비회원의 기능을 구분할 수 있습니다.<br>
        SessionAuthentication 을 이용 신원 확인 후 권한을 부여합니다.<br>
 

        |user|Permission Class|Available|
        |---|---|---|
        |no login|ReadOnly|읽기 가능|
        |login|IsAuthenticated|읽기 & 쓰기 가능|
        |login&owner|IsOwnerOrReadOnly |읽기 & 쓰기 & 해당 게시글 수정 가능|
      

  + **쿠팡 장바구니 상품 가격 저장**<br>
    + **ERD**<br>
      <img src=https://user-images.githubusercontent.com/59391473/204123286-7d19c1ca-0955-4da5-8117-a9124cf2c785.png width="500" height="200"/>
      <img src=https://user-images.githubusercontent.com/59391473/204123271-dbd6c817-b0d4-4ad7-9ff3-5a360cc10916.png width="300" height="250"/>
    + **장바구니 상품 update 시퀀스 다이어그램**<br>
    <img src=https://user-images.githubusercontent.com/59391473/204119067-8cf40224-6da0-4807-84ca-394aeaaa03f2.png width="700" height="500"/><br>
      selenium을 이용한 크롤링으로 쿠팡 장바구니 속 상품의 정보를 가져옵니다.<br> 
      
      이용자들의 장바구니 속 상품을 모두 product 테이블에 중복되는 크롤링을 방지했습니다. <br>
      이때 상품별로 이용자 테이블을  One-to-many의 관계로 생성하여 자신의 장바구니에 담긴 상품만 조회 가능하도록 했습니다.<br>
      job에 등록하여 3 시간에 한번 크롤링하며 하루의 최저 금액을 저장하고 일별 최저가를 보여줍니다.<br>
      
    + **상품 정보 쿼리 최적화**
      + `product` 의 `wisher` 로 장바구니에 등록 된 상품인지 판별한다. <br>
         이때 `product` 에서 `wisher`를 정참조 하기 대문에 `select_related`로 캐싱하여 쿼리를 줄일 수 있다.<br>
      + **소스코드 예제**
        ```python
        class MyProductDataView(APIView):
        permission_classes = [IsAuthenticated]
        authentication_classes = [SessionAuthentication]
        serializer_class=ProductDataSerializer
        def get(self, request):
            queryset = ProductData.objects.select_related('wisher').filter(wisher=request.user.id)
            serializer=ProductDataSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        ```
      + **변경 전**
      <img src=https://user-images.githubusercontent.com/59391473/204297520-7e8a1cdc-5c1a-4b34-8c2b-605ddaabe80f.png width="1000" height="300"/><br>
      <br>
      
      + **변경 후**
      <img src=https://user-images.githubusercontent.com/59391473/204297082-4bcaac23-279b-4c0a-8a10-739df0bdc41d.png width="1000" height="250"/><br>
      <br>
        objects를 하나하나 가져오던 방식에서 한번에 가져오는 방식으로 바뀜

  + **블로그**<br>
    + **ERD**<br>
      <img src=https://user-images.githubusercontent.com/59391473/204120438-cc95fe4b-114b-4273-aca6-6bf8b067cfd9.png width="300" height="300"/>
      <img src=https://user-images.githubusercontent.com/59391473/204120494-9f34aaee-8032-42d2-a888-5f1c49996432.png width="300" height="250"/>
      <img src=https://user-images.githubusercontent.com/59391473/204120533-f7d44137-bbcd-41ec-bc38-458210a016a2.png width="300" height="250"/><br>
      
    + **detail**<br>  
      product 테이블에 있는 상품을 one to one 으로 연결하여 해당 주제의 글을 쓸 수 있습니다.
      post와 comment, liker를 many-to-many 관계로 구현했습니다<br>
      django 의 orm 을 이용하여 유저가 댓글을 달거나 좋아요를 누른 글을 역참조 할수 있습니다<br>


## 5. URL 명세
  + **5. 1. /account**

|CRUD|HTTP|URL|
|---|---|---|
|로그인|POST|/login|
|로그아웃|GET|/logout|
|회원가입|POST|/register|
|카카오 회원가입|GET|/kakao/login|

  + **5. 2. /blog**

|CRUD|HTTP|URL|
|---|---|---|
|게시글 조회|GET|/posts|
|게시글 등록|POST|/posts|
|특정 게시글 조회|GET|/posts/{post_id: int}|
|내 게시글 조회|GET|/user-posts|
|해당 게시글 댓글 조회|GET|/posts/{post_id: int}/comment|
|해당 게시글 댓글 등록|POST|/posts/{post_id: int}/comment|
|해당 게시글 좋아요|GET|/post/{post_id: int}/like|
|해당 게시글 좋아요 회원 조회|GET|/post/{post_id: int}/like-list|
|등록 상품 전체 조회|GET|product|
|쿠팡 장바구니 업데이트|GET|/product/my|
|상품 가격 조회|GET|/price/{int:product_id}|
|Product job init|GET|/product-data/|


## 6. UML 명세🧾🗂
  + **6. 1. 클래스 다이어그램**<br>
    <img src=https://user-images.githubusercontent.com/59391473/204120205-34ec9d48-9101-4ccc-8e56-1ba19b0e06fd.png width="500" height="700"/><br>
## 7. Trouble Shooting ✨
  <details>
  <summary>상품 데이터 중복 이슈</summary>
  <div markdown="1">   
  서로 다른 이용자가 같은 상품을 담았을 때 상품 정보가 중복되어 데이터베이스 낭비가 발생했다.<br>

  product 모델에 url 속성을 추가하여 상품 당 한번만 정보를 가져오도록 변경했다. <br>
  사용자의 장바구니를 주기적으로 크롤링하여 업데이트 -> product 모델을 주기적으로 크롤링 <br>
  로그인을 생략한 크롤링으로 실행시간을 줄이고, 데이터 중복을 방지 할 수 있었다.<br>
  </div>
  </details>

  <details>
  <summary>주기적 실행</summary>
  <div markdown="1">   
  ```crontab``` 과 ```background_task``` 를 이용하여 구현 했으나, django 3버전부터 지원하지 않는 문제가 발생했다. <br>
  ```apscheduler``` 로 대체하여 해당 url 로 접근 시 주기적으로 크롤링 시작하는 방법으로 변경했다.<br>
  </div>
  </details>
   <details>
  <summary>EC2 CPU 성능</summary>
  <div markdown="1">   
  EC2에서 가장 작은 micro 인스턴스를 선택해 배포했는데 서버의 성능이 너무 느리려 크롤링을 하는데 문제가 발생했다.<br>
  cpu 메모리 용량이 더 큰 medium 인스턴스로 재 가동했다.<br>
  </div>
  </details>
  
  <details>
  <summary>queryset 을 리스트로 가져올 때에 발생한 이슈</summary>
  <div markdown="1">   
  filter 를 통해 가져오는 object 가 두개 이상일 때 serializer에서 queryset 값을 찾지 못했다. <br>
  serializer 에서 `many=True` 값을 주어 해결했다. <br>
  </div>
  </details>
  
  <details>
  <summary>AWS 비용 이슈</summary>
  <div markdown="1">   
  한달 간 ec2와 RDS를 구동했더니 5만원이 넘는 비용이 청구되었다.
  EC2 보다는 RDS의 영향이 큰것으로 보인다. 
  둘 모두의 인스턴스를 종료했다.
  </div>
  </details>
   <details>
  <summary>secrte_key 보안</summary>
  <div markdown="1">   
  로그인과 회원가입에 쓰이는 secret키를 앱 내에 두고 배포하면 보안문제가 발생한다.<br>
  secrets.json 파일을 만들어 secret 키 등을 넣어 배포했다.<br>
  값을 가져오는 utils.py 파일을 만들고 다른 파일에서 import 하여 사용할 수 있다.<br>
  </div>
  </details>
  
# 키즈노트 BE개발 사전과제
연락처의 crud, 라벨의 crud, 연락처와 라벨의 매핑을 처리합니다.
- 연락처의 목록 (주소록)을 조회할 수 있습니다. 개별 연락처 조회화는 달리 메모, 주소, 생일, 웹사이트 정보가 표시 되지 않습니다.
- 연락처의 목록 조회시 커서 기반으로 페이징이 적용됩니다.
- 연락처의 목록 조회시 이름, 이메일, 전화번호를 기준으로 오름차순 / 내림차순 정렬할 수 있습니다. 별도로 정렬을 변경하지 않으면 생성시점 기준으로 정렬합니다.
- 연락처를 생성, 조회, 수정, 삭제하는 것이 가능합니다. 
- 연락처에는 하나 이상의 라벨을 적용할 수 있습니다.
- 라벨을 생성, 조회, 수정, 삭제하는 것이 가능합니다.

  

## 프로젝트의 실행
linux bash 에서 아래의 명령을 입력하여 어플리케이션을 실행합니다.  

(각 환경 변수는 DB의 root 사용자, `kidsnote` 사용자의 비밀번호로 사용되며 값은 원하는 값으로 변경 가능합니다.)

```
export MYSQL_ROOT_PASSWORD=J8pLm4qA9z
export MYSQL_PASSWORD=2Bw9kLp6Rs
docker-compose up --build
```

실행되는 사항은 아래와 같습니다.  

1. mysql
* MySQL DB 컨테이너가 생성됩니다.
* `kidsnote_contact` datebase를 생성합니다.
* `kidsnote_contact` database에 접근 가능한 `kidsnote` 사용자를 생성합니다. 
* `db/1_schema.sql` 파일을 사용하여 Django Rest Framework 앱에서 사용할 테이블을 생성합니다.
* `db/2_data.sql` 파일을 사용하여 테이블에 목데이터를 삽입합니다.

2. web
* backend 폴더에 정의된 Django Rest Framework 앱을 실행합니다.
* DB는 1번에서 생성한 mysql 서비스를 사용합니다.
* 80번 포트를 통해 웹어플리케이션에 접속할 수 있도록 설정합니다.

초기화가 완료된 이후 브라우저에서 아래의 주소에 접속하여 api에 접근할 수 있습니다.
```
http://localhost/
(또는 http://127.0.0.1/)
```

## API 개발 사항
아래의 링크에 접속하여 swagger docs를 확인할 수 있습니다.  
```
http://localhost/api/schema/swagger-ui/
```
![swagger이미지](https://github.com/minor7295/backend-pre-task/blob/master/img/swagger%20%EC%9D%B4%EB%AF%B8%EC%A7%80.png?raw=true)

## 디렉토리 구조
```
.
├─backend
│  ├─api
│  │  ├──_
│  │  ├─apps.py : 앱을 프로젝트에 등록할 때에 사용합니다.
│  │  ├─models.py : django orm 모델을 정의합니다.
│  │  ├─serializers.py : django orm과 json의 상호변환을 담당합니다.
│  │  ├─views.py : model을 기반으로 CRUD를 처리합니다.
│  │  └─tests.py : view의 동작을 검증합니다.
│  │─apps
│  │  ├─apps.py : 앱을 프로젝트에 등록할 때에 사용합니다.
│  │  └─routers.py : viewset의 view와 http메소드를 연결합니다. 수정작업을 put메소드로 통일합니다.
│  └─conf
│    ├─settings.py : 프로젝트 설정들을 담은 파일입니다. 
│    ├─urls.py : viewset과 view를 url에 연결합니다.
│    ├─asgi.py : asgi 실행시 사용합니다.
│    └─wsgi.py : wsgi 실행시 사용합니다.
├─db
│  ├─1_schema.sql: MySQL DB의 테이블 생성에 사용되는 파일입니다.
│  └─2_data.sql: MySQL DB에 목데이터를 삽입할 때 사용되는 파일입니다.
│─Dockerfile : backend폴더의 소스코드를 docker image로 빌드합니다.
│─docker-compose.yml : mysql과 DRF앱을 실행합니다.
└─manage.py : 테스트 환경에서 앱를 실행할 때 사용합니다.
```
## DB / Model 설계
[ERD](https://drive.google.com/file/d/1o18rH3gINEhkL-HfPFFoYVyzAuwC8Qwe/view?usp=sharing)
![ERD이미지](https://github.com/minor7295/backend-pre-task/blob/master/img/erd%20%EC%9D%B4%EB%AF%B8%EC%A7%80.png?raw=true)

1) 테이블 구성: `tb_contact`(연락처), `tb_label`(라벨), `tb_contact_label`(연락처, 라벨 매개) 등 총 3개의 테이블로 구성되어있습니다. Django ORM Model에서 위의 테이블은 각각 `Contact`, `Label`, `ContactLabel` 모델로 매핑됩니다.
3) 인덱스 처리: `name`(이름),`email`(이메일), `phone`(전화번호) 필드 기준 정렬 속도를 높이기 위해 `tb_contact` 테이블에 인덱스를 설정하였으며, 중복된 전화번호가 등록되지 않도록 `phone` 필드 기준으로 유니크 인덱스를 설정하였습니다. Django ORM model에서 모델 내부 `Meta` class에서 `indexes`, `constraints`로 표현됩니다.
3) M : N 관계 처리: `tb_contact`테이블의 `contact_id`필드, `tb_label`테이블의 `label_id`필드를 각각 `tb_contact_label`테이블의 동일명의 필드와 외래키로 연결하여 연락처와 라벨의 연결관계를 표현합니다. Django ORM model에서 `ManyToManyField`필드로 표현됩니다.
4) url : `tb_contact`테이블의 `profile`(프로필이미지 url), `website`(웹사이트) 필드는 Django ORM model의 URLField를 사용하여 표현합니다. MySQL DB에서는 varchar 필드로 표현되며, 크롬 기준 최대 url길이인 2083자로 설정하였습니다.
5) email : `tb_contact`테이블의 `email`필드는 Django ORM model의 EmailField를 사용하여 표현합니다. MySQL DB에서는 varchar(254) 필드로 표현됩니다.

## serializer 구성
1) ModelSerializer: Django ORM모델을 통해 DB record와 json 데이터를 상호변환하기 위해 Django Rest Framework의 ModelSerializer를 사용했습니다.
2) Nested Serializer: 연락처별로 적용된 라벨들을 표현하기 위해 연락처 목록, 연락처 상세정보를 담당하는 `ContactListSerializer`와 `ContactDetailSerializer`에 라벨을 담당하는 `LabelSerializer`를 필드로 추가하였습니다.
2) 필드 추가 정의: 연락처 목록에서는 `company`(회사)와 `position`(직책)을 하나의 필드로 합쳐서 표현하기 위해 `company_position`이라는 필드를 추가하였습니다. list view에서 queryset을 재정의하며 추가된 `company_position`필드를 json으로 변환하게 됩니다.
2) 필드 제한: 연락처 목록에서는 `Meta` 클래스의 `fields` 프로퍼티에 json으로 변환할 필드목록을 명시하여 상세정보를 생략합니다.
3) nested serializer의 사용
4) 목록 serializer 와 상세 serializer의 분리

## view 구성
1) ModelViewSet의 사용: CRUD 구현은 Django RestFramework의 ModelViewSet을 상속하여 구현합니다. 단, 개별 라벨 정보와 같이 retrieve view의 필요성이 없는 경우 api에서 제외하기 위해 ModelViewSet의 일부 Mixin을 상속하여 구현합니다.
3) get_serializer_class 재정의: retrieve, list view와 custom action view등 서로 다른 view에서의 응답형태를 다르게 처리하기 위해 action별로 serializer class를 다르게 반환합니다.
4) filter_queryset 재정의를 통한 필드 추가: 두 필드를 합친 필드를 생성하는 등 필드 구성의 변경이 필요한 경우 ViewSet 내부에서 queryset을 변형합니다.


## 프로젝트 설정
2) 페이지네이션, 정렬: 인피니트 스크롤 구현을 위해 기본적으로 CursorPagination을 적용합니다. 페이지네이션의 적용 필요성이 없는 view에서는 이 설정을 제거합니다. 
4) router 재정의: api의 간결성을 강화하기 위해, 수정 작업은 put/patch를 모두 사용하지 않고, put작업으로 통일합니다.

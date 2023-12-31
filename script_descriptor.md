### Аннотация

    Файл содержит описание структуры элементов дескриптора
    скриптов и применения дескриптора для настройки экземпляров сценариев.

### Что такое "дескриптор" и его назначение 
    
    Дескриптор содержит описание скрипта и используется клиентскими приложениями (далее - Клиент) для динамического формирования интерфейса настройки.

#### Формат

    Дескриптор является параметром скрипта и представляет собой строку в формате json, **обязателеную** для всех скриптов.
    Храниться в БД settings в таблице scripts или в виде файла (на усмотрение разработчиковв скриптов).

    Дескриптор содержит:
        -   имя скрипта **_"name"_**, 
        -   его текстовое описание **__"descrpition"__** для пользователя, которое он увидит в интерфейсе
        -   текстовый комментарий разработчика **__"comment"__** для пользователя, которое будет скрытот под спойлером
        -   массив параметров **_"params"_** скрипта с описаниями и настройкам, значения для которых настраиваются пользователем.
        -   массив пост-параметров **_"post"_** скрипта, значения для которых устанавливаются веб-сервисом в зависимости от заданных пользователем params
        -   значение **_"longdetector"_**, которое будет присвоено создаваемой в результате настройки данного скрипта зоне, 
            которая будет ассоциирована с экземпляром настроенного сценария script_instance 
    
    Массив параметров - это то, что необходимо передать для настройки экземпляра сценария. 
    Данные параметры понадобятся при инициализации настроенного сценария для формирования контекста и подписки (НЕ формируется на стороне клиентского приложения).

    Каждый элемент массива параметров (далее - Параметр) в свою очередь также является json-объектом c фиксированным набором ключей (далее - Свойства параметра), 
    которые должен знать Клиент для корректного формирования интерфейса и передачи заданных пользователем параметром для настройки скрипта.
    
#### Свойства параметров из дескриптора:

##### Обязательные

**name**        - ключ/имя, которое будет передано Клиентом с введенным или выбранным в интерфейсе значением при настройке сценария. 
                Данное свойство должно содержать ключ, который скрипт должен понимать и ждать на входе при инициализации.

    Определенные значения ключа name должны быть зарезервированы для параметров, которые должны быть сохранены в таблицы с БД отдельно от натсроенного контекста сценария:
        name            -   имя создаваемой зоны (записывается в таблицу Zone)
        comment         -   комментарий к зоне (записывается в таблицу Zone)
        delay           -   время задержки на вход (записывается в таблицу Zone)
        active          -   состотяние активности зоны (вкл/выкл) (записывается в таблицу Zone)
        partition       -   раздел, в который будет помещена зона (записывается в таблицу Zone)
        resources       -   для массива ресурсов, связываемых со сценарием-зоной (их будет анализировать веб-сервис дя определения доступности скрипта для создания зоны устройства)
        %resource%      -   должен содержать в своем имени параметр выбора связанного ресурса (записываются в таблицу ScriptInstance_Resources) 

**type**        - тип параметра, от которогго зависит элемент инпута и тип  данных значения, которое принимает данный параметр 
                (доступные значения "int", "float", "string", "boolean", "array", "object").


    Доступные типы параметров: 
	
    int                 - стандартный инпут, тип данных - целое число
	float               - стандартный инпут, тип данных - число с плавающей точкой
	text                - стандартный инпут, тип данных - строка

	select              - выбор одного варианта из списка на выбор, варианты на выбор в res:list, res: list_prep или res: list_gen 
                        (обязательно одно из трех). 
                        В ответе передается значение, полученное из выбранного элемента res:list, res: list_prep или res: list_gen.
                        Инпут по умолчанию -  дроп.
                        Тип данных - тот же, который был передан для value бэкэндом.
    select_zone         - выбор зоны из списка зон на выбор (остальное аналогично select)
    select_partition    - выбор раздела из списка разделов на выбор (остальное аналогично select)
    select_device       - выбор девайс-ресурса из списка девайс-ресурсов на выбор (остальное аналогично select)
    select_dresource    - выбор девайса из списка девайсов на выбор (остальное аналогично select)
    select_id           - выбор идентификатора из списка идентификаторов на выбор (остальное аналогично select)
    list                - выбор нескольких вариантов из списка на выбор, варианты на выбор в res:list, res: list_prep или res: list_gen. 
                        в ответе передается массив значений, полученных из выбранных элементов res:list, res: list_prep или res: list_gen.
                        Инпут по умолчанию - чекбокс лист.
                        Тип данных - массив, элементы массива имеют тот же тип, который был передан в value.
	list_zone           - выбор нескольких зон из списка на выбор (остальное аналогично list)
    list_partition      - выбор нескольких разделов из списка на выбор (остальное аналогично list)
    list_device         - выбор нескольких девайсов из списка на выбор (остальное аналогично list)
    list_dresource      - выбор нескольких девайс-ресурсов из списка на выбор (остальное аналогично list)
    list_id             - выбор нескольких идентификаторов из списка на выбор (остальное аналогично list)
    switch              - переключатель, может использоваться без res: list_prep
	                    Тип данных по умолчанию boolean, возвращает true/false (но может быть изменен на то, что содержится в res: list_prep).
    group               - группа параметров, требуется для того, чтобы отобразить несколько параметров для настройки через один компонент ui 
                        или сгруппировать их в интерфейсе
                        (например,  - для выбора списка ресурсов различного типа,
                                    - для настройки температурного режима в определенный день или временных интервалов на каждый день недели).
                        Содержит в себе массив вложенных параметров. 
                        Структура идентична массиву элементов дескриптора.
                        Отсутствует в массиве настроенных параметров (массив содержит сразу то, что внутри group)

                        Важно! Связываемые со сценарием ресурсы должны всегда должны быть в group в "name":"resources"  
                        
    примечание: параметрам всех типов в результате настройки присваиваются значения того типа, который требуется конкретным параметром.


##### Необязательные

**def**         - строка, значение параметра по умолчанию.
**req**         - флаг, определяющий обязательно или не обязательно передавать значение для данного параметра
**fxd**         - флаг, определяющий можно или нельзя изменять значение для данного параметра, если уже имеется значение, сохраненное в массиве параметров
**invisible**   - флаг видимости параметра (для передачи значений по умолчанию из дексриптора)
**group**       - используется только для параметров типа group и time_group в качестве ключа, внутри которого содержится массив параметров, входящих в данную группу
**res**         - свойство, содержащее данные, которые будет использовать input-компонент клиентского интерфейса для формирования самого интерфейса настройки
                и массива возвращаемых параметров.
                представляет собой json-объект с фиксированным набором допустимых ключей (далее Опции), значение каждого из которых определяет 
                либо свойство формируемого компонента интерфейса и его поведение, либо алгоритм обработки данного ресурса веб-сервисом. 
                ***ВАЖНО***  
                все строковые значения для всех Опций должны храниться на англ языке и будут использоватся интерфейсом веб-приложения 
                в качестве ключей для локализации.
	
    доступные свойства res:
    
    //19.08.2023
    label           - текстовое значение заголовка label для ui-компонента параметра
    placeholder     - значение для placeholder'a
    hint            - подсказка пользователю при вводе строковых данных, отображается под полем ввода (напр,  можеет содержать подсказку с единицами измерения или допутстимыми величинами параметра)
    regex           - регулярное выражение, устанавливающее ограничивающие правила для вводимых данных, строка
    comment         - текстовое поле с подсказкой, отображается в тултипе
    error           - текст ошибки ввода
    form            - тип инпута, заменяющий инпут по умолчанию
                    (м.б. 
                    textarea - для text, 
                    radio - для типа select по умолчанию  
                    drop    - для типа list, 
                    therm - для типа группа, для отображения термостата),
    text_color      - цвет текста ввода, rgbhex 	
    text_size       - размер текста ввода, rgbhex 	
    cursor_color    - цвет курсора, rgbhex 	

    list            - массив целочиcленных значений [int] предоставляемых на выбор пользователю в ui, полученных из бд 
                    или подготовленных вручную.
                    ui сам выбирает формат представления этого списка в зависимости от типа параметра, используя значения из массива, 
                    и эти же значения возвращает в качестве значений парамтера после выбора пользователем. 

    list_prep       - массив json-объектов с подготовленными данными для формирования в ui cписка на выбор пользователю.
                    каждый элемент list_prep представляет собой объект с ключами value и caption.
                    в этом случае пользователю отображается caption, 
                    а в качестве значения параметра для настройки передается значение value 
                    или массив value (в зависимости от типа параметра) выбранного пользователем элемента списка из list_prep.

    list_gen        - массив json-объектов с данными, полученными из БД конфигурации, 
                    необходимыми для формирования в ui cписка на выбор пользователю.
                    в этом случае пользователю отображается строка, сформированная при помощи format_tpl и format_reg, 
                    а в качестве значения параметра для настройки передается значение ключа,  указанного в return 
                    или массив таких значений (в зависимости от типа параметра) выбранного пользователем элемента списка из res: list_gen.
    format_tpl      - шаблон строки, выводимой в ui, для отображения элементов из списка res: list_gen.
    format_reg      - регулярка для корректной замены ключей в format на данные, полученные в res: list_gen, перед отображением в ui (обязательно при наличии format).
                    строки, найденные в format_tmpl при помощи регулярного выражения из format_reg должны быть подмениться на значения
                    соответствующих ключей из объектов массива res: list_gen.
    * database      - массив запросов в бд, которые формируют итоговый список данных помещаемый в res: list_gen или res: list путем конкатенации всех полученных списков.
    Каждый элемент масссива содержит:
    selector        - запрос, который необходимо осуществить в бд, для получения массива возможных значений параметра.
                    Данные из результата запроса в БД формируют массив res: list_gen или res: list.
                    Обязательно должен содержаться в каждом элементе массива внутри database. 
    values          - массив значений, используемых в качестве ключей при формировании res: list_gen.
                    Необязательно содержится в каждом элементе массива внутри database. 
                    Если отсутствует,  то в результате селекта формируется res: list.

    *   -    заменяется вместе со всем содержимым на res: list_gen или res: list.  

    return          - содержит ключ, значение которого требуется возвращать для настройки выбранного параметра сценария.
                    Существует только при наличии database, замененного на res: list_gen, 
                    для того, чтобы понимать, значение какого из ключей внутри объетов из массива res: list_gen
                    может являться значением параметра.

#### Свойства пост-параметров из дескриптора:

##### Обязательные

**name**            - ключ/имя, которое будет использовано веб-сервисом при сохранении значения ключа с именем данного параметра,
                    перед его добавлением в массив параметров из контекста сценария.
                    Данное свойство должно содержать ключ, который скрипт должен понимать и ждать на входе при инициализации.

**selector**        - запрос, который необходимо осуществить в бд, для получения единственно верного значения параметра.
                    Данные из результата запроса в БД буду записаны веб-сервисом в качетсве значения ключа value с установленным значением данного параметра, 
                    перед его добавлением в массив параметров из контекста сценария.

##### Необязательные

**variables**       - массив ключей параметром из массива params, установленные пользователем значения которых требуется использовать в качестве переменных для запроса из 
                    ключа selector.



#### Использование дескпритора

    1. Перед тем, как передать дескриптор клиенту по запросу SCRIPT, веб-сервис ищет в нем все параметры, которые содержат опцию database и заменяет данную опцию на list_gen со 
    списком значений параметра, полученным из БД конфигурации.

    
    2. Получив descriptor, Клиент парсит объект с ним, и каждый параметр без свойства <invisible: true> превращает в форму ввода данных и добавляет в общее окно 
    настройки сценария.

    После ввода значений параметров пользователем и валидации их в форме ввода, заданные значения передаются веб-сервису в команде настройки сценария
    в виде json-массива с ключом "params", соддержащего объектов вида
    {
        "name": "name_from_descriptor",
        "value": value_from_ui_in_certain_type
    }
    
где

    **name_from_descriptor**                    - ключ/имя параметра, полученное из свойства "name" данного параметра (то, что должен понимать скрипт), 
    **value_from_ui_in_certain_type**           - введенное или выбранное пользователем значение, определенного типа, зависящего от типа параметра.


    Переданный массив параметров сохраняется в БД в таблице script_instances в столбце context. 
    А через таблицу zones cценарий связывается с реализуемой им зоной.
    Значения параметров из group с "name": "resources" записываться в таблицу связи скрипт_инстанс - ресурс.

    При инициализации сервис скриптов получает из БД сохраненный массив параметров для настроенного сценария, 
    при необходимости дополняя его перед этим парами "ключ": "значение", содержащими данные из различных таблиц
    id, type, parent и тд (при необходимости) или целиком передавая данные о зоне в виде объекта.
     

#### Пример использования дескриптора:

        
    Пример 1:


        **Содержание дескриптора скрипта сложного детеектора Открытие окна**

        {
            "name": "Открытие окна",
            "description": "Реализация логики работы охранной зоны, оповещающей об открытии окна",
            "longdetector": 32,
            "comment": "Тут какой угодно коммент вообще любой, а переносы строк можно вот так делать \n и на новой строке, не обязательно использовть массив",
            "params": [
                {
                    "type": "text",
                    "name": "name",
                    "req": true,
                    "res": {
                        "label": "Имя зоны",
                        "hint": "Введите имя зоны",
                        "reg": "^.{3,20}$"
                    },
                    "comment": "Параметр должен попасть в Name в таблицу Zone."
                },
                {
                    "type": "text",
                    "name": "comment",
                    "req": false,
                    "res": {
                        "label": "Комментарий",
                        "reg": "^.{3,20}$"
                    },
                    "comment": "Параметр \"name\": \"comment\" должен попасть в Comment в таблицу Zone."
                },
                {
                    "type": "switch",
                    "name": "active",
                    "req": true,
                    "def": true,
                    "res": {
                        "label": "Включить зону"
                    },
                    "comment": "Параметр \"name\": \"active\" должен попасть в Active в таблицу Zone."
                },
                {
                    "type": "select",
                    "name": "partition",
                    "req": true,
                    "res": {
                        "label": "Select partitions",
                        "format": "&lt;{id}&gt; &lt;({name})&gt;",
                        "format_reg": "<([^<]*)\\{([\\w\\%\\.]+)(?>@([\\w]+))?\\}([^>]*)>",
                        "return": "id",
                        "database": [
                            {
                                "values": ["id", "name"],
                                "selector": "SELECT Partition.id, Partition.name FROM Partitions WHERE Partitions.Type = 1"
                            }
                            ]
                        },
                    "comment": "Запрос должен выбрать из таблицы Partition список разделов определенного или определенных типов,
                        в которые может быть помещена данная зона.
                        Для формирования запроса надо выполниьт запрос из selector.
                        Результат должен быть возвращен в параметре \"res\" : [{object}], 
                        object формируется динамически -,
                        в качестве ключей берутся значения из values, а в качестве значений то,
                        что получено в результате селекта, из столбца, соответствующего порядковому номеру ключа в массиве values"
                },
                {
                    "type": "int",
                    "name": "delay",
                    "req": true,
                    "def": 1,
                    "res": {
                        "label": "Задержка",
                        "hint": "Задержка на взятие"
                        },
                    "comment": "Вы можете установить значение времени задержки на взятие для данной зоны"
                },
                {
                    "type": "group",
                    "name": "resources",
                    "params": [
                        {
                            "type": "select",
                            "name": "resource0",
                            "req": true,
                            "res": {
                                "label": "Ресурс:",
                                "hint": "Выберите ресурс",
                                "format_tpl": "&lt;{label}&gt; &lt;(устройство - {device_type} &lt;(device_sn)&gt;)&gt;",
                                "format_reg": "<([^<]*)\\{([\\w\\%\\.]+)(?>@([\\w]+))?\\}([^>]*)>",
                                "return": "res_id",
                                "database": [
                                    {
                                        "values": ["id", "res_id", "caption", "device_id", "device_type", "device_sn"],
                                        "selector": "SELECT r.id, rh.id, r.db_caption, d.id, d.type, d.sn FROM DeviceResources as r 
                                            LEFT JOIN ResourceHub as rh ON ResourceHub.id = DeviceResources.ResourceId LEFT JOIN Device as d ON Device.id = DeviceResources.DeviceId 
                                            LEFT JOIN ResourceHelper as r_db ON DeviceResources.id = ResourceHelper.ResourceId WHERE r.type = 8"
                                    },
                                    {
                                        "values": ["id", "res_id", "caption"],
                                        "selector": "SELECT z.id, rh.id, z.caption FROM Zones as z LEFT JOIN ResourceHub as rh ON ResourceHub.id = Zones.ResourceId  WHERE z.type = 8"
                                    }
                                ]
                            },
                            "comment": "Вываливает первый список ресурсов, подходящих для создания скрипта и данной зоны.
                                Количество списков в группе resources зависит от того,  сколько ресурсов в принципе надо для скрипта.
                                В данном случае на выбор даются Бинарные сенсоры и зоны охранных ШС.
                                Ресурс, который выберет пользователь, должен связаться с создаваемым scriptinstance через таблицу script_instance_resource"
                        },
                        {
                            "type": "select",
                            "name": "resource1",
                            "req": true,
                            "invisible": true,
                            "default": "0",
                            "res": {
                                "return": "res_id",
                                "database": [
                                    {
                                        "values": ["id", "res_id", "caption", "device_id", "device_type", "device_sn"],
                                        "selector": "SELECT r.id, rh.id, r.db_caption, d.id, d.type, d.sn FROM DeviceResources as r 
                                            LEFT JOIN ResourceHub as rh ON ResourceHub.id = DeviceResources.ResourceId 
                                            LEFT JOIN Device as d ON Device.id = DeviceResources.DeviceId 
                                            LEFT JOIN ResourceHelper as r_db ON DeviceResources.id = ResourceHelper.ResourceId WHERE r.type = 23",
                                    }
                                ]
                            },
                            "comment": "Какой-то комментарий"
                        }
                    ]
                }
            ],
            post": [
                {
                    "variables": ["resource0", "resource1"],
                    "name": "resource2",
                    "selector": "SELECT r.id FROM DeviceResources as r LEFT JOIN ... WHERE some_id = ? AND something = ?"
                },
                {
                    "variables": ["resource1"],
                    "name": "resource3",
                    "selector": "SELECT r.id FROM DeviceResources as r LEFT JOIN ... WHERE something = ?"
                }
            ]
            
        }
            
        **Массив параметров, заполненный значениями:**
    
        "params": [
            {"name":"name", "value":"Окно в зале"},
            {"name":"comment", "value": "В датчиике надо поменять батарейку, так как поставили старую при настройке"},
            {"name":"active", "value": true}
            {"name":"partition", "value": 1}
            {"name":"delay", "value": 60}
            {"name":"resource0", "value": 15} 
            {"name":"resource1", "value": 11} 
        ]


    
    Пример 2:

        **Содержание дескриптора скрипта Полив**
        
        {
        "name": "Полив",
        "description": "Сценарий включения полива по расписанию на указанную продолжительность времени",
        "params": [
            {
               "type":"text",
               "name": "name",
               "req": "true",
               "res":" {
                    "label":"Название",
                    "hint": "Минимум 3 символа, максимум - 20",
                    "reg":"^[A-Za-z0-9.]+$"
               }
            },
            {
                "type":"int",
                "name": "duration_value"
                "def":"60"
                "res":{
                    "label":"Продолжительнсть полива",
                    "hint":"Минуты"
                }
            },
            {
                "type":"list",
                "name":"period",
                "req":"true",
                "res":{
                    "label": "Периодичность полива",
                    "list_prep": [{
                                "caption": "Every monday",
                                "value": 1
                            },{
                                "caption": "Every tuesday",
                                "value": 2
                            },{
                                "caption": "Every wednesday",
                                "value": 4
                            },{
                                "caption": "Every thursday",
                                "value": 8
                            },{
                                "caption": "Every friday",
                                "value": 16
                            },{
                                "caption": "Every saturday",
                                "value": 32
                            },{
                                "caption": "Every sunday",
                                "value": 64
                            },{
                                "caption": "Even days",
                                "value": 0
                            },{
                                "caption": "Odd days",
                                "value": 128
                            },{
                                "caption": "Everyday",
                                "value": 65
                            },{
                                "caption": "Every 2 days",
                                "value": 66
                            },{
                                "caption": "Every 3 days",
                                "value": 68
                            },{
                                "caption": "Every 4 days",
                                "value": 72
                            },{
                                "caption": "Every 5 days",
                                "value": 80
                            },{
                                "caption": "Every 6 days",
                                "value": 96
                            }
                        ]
                }
            },
            {
                "type":"int",
                "name":"start_time",
                "req":"true"
                "res":{
                    "label":"Начало полива",
                }
            }
        ]
    
        
        **Массива параметров, заполненный значениями:**
    
        "params": [{"name":"name", "value":" Полив моего любимого газона"},
            {"name":"duration_value", "value": 30},
            {"name":"period", "value": 3}
            {"name":"start_time", "value": 1035} // 17:15, но время в минутах
        ]


import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect('pc_shop.db')
cursor = conn.cursor()

# создание таблиц
cursor.execute('''
create table categories (
    id integer primary key autoincrement,
    name text not null unique,
    description text
)
''')

cursor.execute('''
create table products (
    id integer primary key autoincrement,
    product_name text not null,
    price real not null,
    stock_quantity integer default 0,
    specs text,
    brand text,
    category_id integer not null,
    foreign key (category_id) references categories(id)
)
''')

cursor.execute('''
create table customers (
    id integer primary key autoincrement,
    full_name text not null,
    email text unique,
    phone text,
    city text,
    registration_date text default current_timestamp
)
''')

cursor.execute('''
create table orders (
    id integer primary key autoincrement,
    customer_id integer not null,
    order_date text default current_timestamp,
    total_amount real not null default 0,
    status text not null default 'pending',
    foreign key (customer_id) references customers(id)
)
''')

cursor.execute('''
create table order_items (
    id integer primary key autoincrement,
    order_id integer not null,
    product_id integer not null,
    quantity integer not null check(quantity > 0),
    price_at_moment real not null,
    foreign key (order_id) references orders(id),
    foreign key (product_id) references products(id)
)
''')

print("таблицы созданы")

# добавление категорий
categories = [
    ('процессоры', 'центральные процессоры intel и amd'),
    ('видеокарты', 'видеокарты nvidia и amd'),
    ('материнские платы', 'материнские платы под intel и amd'),
    ('озу', 'оперативная память ddr4/ddr5'),
    ('накопители', 'ssd и hdd накопители'),
    ('блоки питания', 'блоки питания для пк'),
    ('охлаждение', 'воздушное и жидкостное охлаждение'),
    ('корпуса', 'корпуса для пк'),
]

cursor.executemany('''
    insert into categories (name, description)
    values (?, ?)
''', categories)

print(f"добавлено {len(categories)} категорий")

# каталог товаров (пк комплектующие)
products_catalog = [
    # процессоры
    ('intel core i9-13900k', 58999, 5, '24 ядра, до 5.8 ghz', 'intel', 1),
    ('intel core i7-13700k', 38999, 8, '16 ядер, до 5.4 ghz', 'intel', 1),
    ('amd ryzen 7 7800x3d', 39999, 3, '8 ядер, 3d v-cache', 'amd', 1),
    ('amd ryzen 5 7600x', 22999, 6, '6 ядер, до 5.3 ghz', 'amd', 1),
    # видеокарты
    ('nvidia rtx 4090', 159999, 2, '24gb gddr6x', 'nvidia', 2),
    ('nvidia rtx 4080', 119999, 3, '16gb gddr6x', 'nvidia', 2),
    ('nvidia rtx 4070 ti', 79999, 5, '12gb gddr6x', 'nvidia', 2),
    ('amd radeon rx 7900 xtx', 99999, 2, '24gb gddr6', 'amd', 2),
    ('amd radeon rx 7900 xt', 89999, 3, '20gb gddr6', 'amd', 2),
    # материнские платы
    ('msi b760 tomahawk', 18999, 7, 'lga 1700, ddr5', 'msi', 3),
    ('asus rog strix b650', 22999, 4, 'am5, ddr5', 'asus', 3),
    ('gigabyte z790 aorus', 25999, 3, 'lga 1700, ddr5, pcie 5.0', 'gigabyte', 3),
    ('asrock b760m pro', 12999, 6, 'micro-atx, ddr5', 'asrock', 3),
    # озу
    ('corsair vengeance 32gb', 12499, 15, 'ddr5, 6000mhz', 'corsair', 4),
    ('kingston fury 32gb', 11999, 12, 'ddr5, 5600mhz', 'kingston', 4),
    ('g.skill trident z 16gb', 7999, 10, 'ddr4, 3600mhz', 'g.skill', 4),
    ('teamgroup t-force 16gb', 6499, 8, 'ddr4, 3200mhz', 'teamgroup', 4),
    # накопители
    ('samsung 990 pro 1tb', 12999, 10, 'nvme, 7450mb/s', 'samsung', 5),
    ('wd black sn850x 1tb', 11999, 8, 'nvme, 7300mb/s', 'western digital', 5),
    ('crucial p3 plus 1tb', 7999, 12, 'nvme, 5000mb/s', 'crucial', 5),
    ('kingston nv2 500gb', 4499, 15, 'nvme, 3500mb/s', 'kingston', 5),
    # блоки питания
    ('corsair rm850x', 15999, 6, '850w, 80+ gold', 'corsair', 6),
    ('be quiet! straight power 11', 16999, 4, '750w, platinum', 'be quiet!', 6),
    ('seasonic focus gx-750', 13999, 5, '750w, 80+ gold', 'seasonic', 6),
    # охлаждение
    ('noctua nh-d15', 11999, 7, 'воздушное, 2 вентилятора', 'noctua', 7),
    ('arctic liquid freezer ii 360', 13999, 5, 'жидкостное, 360mm', 'arctic', 7),
    ('deepcool ak620', 5999, 8, 'воздушное, 120mm', 'deepcool', 7),
    # корпуса
    ('lian li lancool 216', 10999, 6, 'mid-tower, 2x160mm', 'lian li', 8),
    ('fractal design meshify 2', 12999, 4, 'mid-tower, tempered glass', 'fractal', 8),
    ('corsair 4000d airflow', 8999, 9, 'mid-tower, mesh front', 'corsair', 8),
]

# добавляем товары
for product in products_catalog:
    cursor.execute('''
        insert into products (product_name, price, stock_quantity, specs, brand, category_id)
        values (?, ?, ?, ?, ?, ?)
    ''', product)

print(f"добавлено {len(products_catalog)} товаров")

# добавление клиентов
customers = [
    ('алексей компьютеров', 'alex@pc.ru', '+79123456789', 'москва'),
    ('елена игровая', 'elena@game.ru', '+79234567890', 'санкт-петербург'),
    ('дмитрий системный', 'dmitry@sys.ru', '+79345678901', 'екатеринбург'),
    ('ольга мониторова', 'olga@mon.ru', '+79456789012', 'новосибирск'),
    ('владимир процессоров', 'vlad@cpu.ru', '+79567890123', 'казань'),
    ('наталья майнингова', 'nataly@mine.ru', '+79678901234', 'москва'),
    ('сергей серверов', 'sergey@server.ru', '+79789012345', 'санкт-петербург'),
    ('анна сборкина', 'anna@build.ru', '+79890123456', 'екатеринбург'),
    ('максим оверхоллер', 'max@overclock.ru', '+79901234567', 'новосибирск'),
    ('татьяна стримерша', 'tanya@stream.ru', '+79012345678', 'москва'),
    ('игорь майнинг', 'igor@mining.ru', '+79123456780', 'иркутск'),
    ('ксюша тестировщица', 'ksu@test.ru', '+79234567891', 'томск'),
]

cursor.executemany('''
    insert into customers (full_name, email, phone, city)
    values (?, ?, ?, ?)
''', customers)

print(f"добавлено {len(customers)} клиентов")

# получаем id клиентов
cursor.execute("select id from customers")
customer_ids = [row[0] for row in cursor.fetchall()]

# получаем товары для генерации заказов
cursor.execute("select id, product_name, price, category_id from products")
products_list = cursor.fetchall()

# функция для случайной даты
def random_date(start_date, end_date):
    time_between = end_date - start_date
    days_between = time_between.days
    random_day = random.randrange(days_between)
    return start_date + timedelta(days=random_day)

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 4, 13)

# генерация заказов
orders_data = []
order_items_data = []
order_counter = 1

for customer_id in customer_ids:
    num_orders = random.randint(1, 4)
    for _ in range(num_orders):
        # выбираем случайное количество товаров в заказе (1-4)
        num_products_in_order = random.randint(1, 4)
        
        # выбираем уникальные товары для заказа (чтобы не было дубликатов)
        selected_products = random.sample(products_list, min(num_products_in_order, len(products_list)))
        
        # статусы заказов с весами
        statuses = ['pending', 'paid', 'shipped', 'delivered', 'cancelled']
        weights = [0.1, 0.15, 0.2, 0.45, 0.1]
        status = random.choices(statuses, weights=weights)[0]
        
        order_date = random_date(start_date, end_date).strftime('%Y-%m-%d')
        
        # сначала создаём заказ с временной суммой 0
        orders_data.append((order_counter, customer_id, order_date, 0, status))
        
        total_amount = 0
        
        # добавляем позиции заказа
        for product in selected_products:
            product_id, product_name, product_price, category_id = product
            quantity = random.randint(1, 3)
            price_at_moment = product_price  # цена на момент покупки
            
            # добавляем небольшую скидку иногда
            if random.random() < 0.3:
                discount = random.uniform(0.05, 0.15)
                price_at_moment = round(product_price * (1 - discount), 0)
            
            order_items_data.append((order_counter, product_id, quantity, price_at_moment))
            total_amount += quantity * price_at_moment
        
        # добавляем стоимость доставки
        shipping_cost = random.randint(300, 800)
        total_amount += shipping_cost
        
        # обновляем сумму заказа в массиве
        orders_data[-1] = (order_counter, customer_id, order_date, round(total_amount, 2), status)
        
        order_counter += 1

print(f"сгенерировано {len(orders_data)} заказов")

# вставляем заказы
cursor.executemany('''
    insert into orders (id, customer_id, order_date, total_amount, status)
    values (?, ?, ?, ?, ?)
''', orders_data)

# вставляем позиции заказов
cursor.executemany('''
    insert into order_items (order_id, product_id, quantity, price_at_moment)
    values (?, ?, ?, ?)
''', order_items_data)

print(f"добавлено {len(order_items_data)} позиций заказов")

# обновляем остатки на складе
for product in products_list:
    product_id = product[0]
    # считаем сколько продали
    cursor.execute('''
        select sum(quantity) from order_items where product_id = ?
    ''', (product_id,))
    sold = cursor.fetchone()[0] or 0
    
    cursor.execute('''
        update products set stock_quantity = stock_quantity - ?
        where id = ? and stock_quantity >= ?
    ''', (sold, product_id, sold))

print("остатки на складе обновлены")

conn.commit()

# финальная статистика
print("\n" + "="*60)
print("итоговая статистика")
print("="*60)

cursor.execute("select count(*) from categories")
print(f"категорий: {cursor.fetchone()[0]}")

cursor.execute("select count(*) from products")
print(f"товаров: {cursor.fetchone()[0]}")

cursor.execute("select count(*) from customers")
print(f"клиентов: {cursor.fetchone()[0]}")

cursor.execute("select count(*) from orders")
print(f"заказов: {cursor.fetchone()[0]}")

cursor.execute("select count(*) from order_items")
print(f"позиций заказов: {cursor.fetchone()[0]}")

# сложные запросы
print("\n" + "="*60)
print("запрос 1: топ клиентов по сумме заказов (только завершённые)")
print("="*60)

cursor.execute('''
    select 
        c.full_name, 
        c.city,
        count(o.id) as orders_count, 
        round(sum(o.total_amount), 0) as total_spent,
        round(avg(o.total_amount), 0) as avg_order
    from customers c
    join orders o on c.id = o.customer_id
    where o.status in ('delivered', 'shipped')
    group by c.id
    having total_spent > 50000
    order by total_spent desc
    limit 10
''')

for row in cursor.fetchall():
    print(f"{row[0]} ({row[1]}): {row[2]} заказов, потрачено {row[3]:.0f}₽, средний чек {row[4]:.0f}₽")

print("\n" + "="*60)
print("запрос 2: средняя стоимость заказа по статусам")
print("="*60)

cursor.execute('''
    select 
        status, 
        count(*) as count, 
        round(avg(total_amount), 0) as avg_amount,
        round(min(total_amount), 0) as min_amount,
        round(max(total_amount), 0) as max_amount
    from orders
    group by status
    order by avg_amount desc
''')

for row in cursor.fetchall():
    print(f"статус '{row[0]}': {row[1]} заказов, средний {row[2]}₽, мин {row[3]}₽, макс {row[4]}₽")

print("\n" + "="*60)
print("запрос 3: самые популярные категории товаров")
print("="*60)

cursor.execute('''
    select 
        cat.name as category,
        count(oi.id) as sold_items,
        round(sum(oi.quantity * oi.price_at_moment), 0) as revenue,
        round(avg(oi.price_at_moment), 0) as avg_price
    from categories cat
    join products p on cat.id = p.category_id
    join order_items oi on p.id = oi.product_id
    join orders o on oi.order_id = o.id
    where o.status in ('delivered', 'shipped')
    group by cat.id
    order by revenue desc
''')

for row in cursor.fetchall():
    print(f"{row[0]}: продано {row[1]} шт, выручка {row[2]}₽, средняя цена {row[3]}₽")

print("\n" + "="*60)
print("запрос 4: средняя цена товара по брендам")
print("="*60)

cursor.execute('''
    select 
        brand,
        count(*) as products_count,
        round(avg(price), 0) as avg_price,
        round(min(price), 0) as min_price,
        round(max(price), 0) as max_price
    from products
    where brand is not null
    group by brand
    having count(*) > 1
    order by avg_price desc
''')

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} товаров, средняя {row[2]}₽, мин {row[3]}₽, макс {row[4]}₽")

conn.close()

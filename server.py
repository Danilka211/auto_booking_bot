# from fastapi import FastAPI, HTTPException
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi import Query
# from typing import List
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from fastapi.templating import Jinja2Templates
# from fastapi import Request, Form
# from datetime import datetime
# from fastapi.responses import RedirectResponse
# from fastapi import status
# from pathlib import Path
# import pathlib
# import json
# import os

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# bookings = []
# BOOKINGS_FILE = "bookings.json"
# CARS_FILE = "cars.json"
# HOLIDAYS = ["2025-01-01",
# "2025-01-02",
# "2025-01-03", 
# "2025-01-04", 
# "2025-01-06", 
# "2025-01-07",
# "2025-01-08", 
# "2025-03-08", 
# "2025-05-01",
# "2025-05-02",
# "2025-05-03",
# "2025-05-08",
# "2025-05-09",
# "2025-05-10",
# "2025-06-12",
# "2025-06-13",
# "2025-06-14",
# "2025-11-03",
# "2025-11-04",
# "2025-12-31"
# ]

# next_booking_id = 1

# def load_bookings():
#     global next_booking_id
#     bookings.clear()  # очищаем глобальный список
#     max_id = 0
#     if os.path.exists(BOOKINGS_FILE):
#         with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
#             loaded_bookings = json.load(f)
#             for b in loaded_bookings:
#                 if "booking_id" not in b:
#                     b["booking_id"] = next_booking_id
#                     next_booking_id += 1
#                 else:
#                     if b["booking_id"] > max_id:
#                         max_id = b["booking_id"]
#                 bookings.append(b)
#             if max_id >= next_booking_id:
#                 next_booking_id = max_id + 1
#     return bookings

# def save_bookings():
#     with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
#         json.dump(bookings, f, ensure_ascii=False, indent=4)

# load_bookings()



# def load_cars():
#     if not os.path.exists(CARS_FILE):
#         return []
#     with open(CARS_FILE, "r", encoding="utf-8") as f:
#         return json.load(f)

# @app.get("/admin/cars", response_class=HTMLResponse)
# def view_cars(request: Request):
#     cars = load_cars()
#     return templates.TemplateResponse("admin_cars.html", {"request": request, "cars": cars})

# @app.post("/admin/cars/delete/{car_id}")
# def delete_car(car_id: int):
#     with open("cars.json", "r", encoding="utf-8") as f:
#         cars = json.load(f)

#     new_cars = [car for car in cars if car["car_id"] != car_id]

#     with open("cars.json", "w", encoding="utf-8") as f:
#         json.dump(new_cars, f, indent=4, ensure_ascii=False)

#     return RedirectResponse(url="/admin/cars", status_code=303)

# @app.get("/admin/cars/edit/{car_id}", response_class=HTMLResponse)
# def edit_car_form(car_id: int):
#     with open("cars.json", "r", encoding="utf-8") as f:
#         cars = json.load(f)

#     car = next((c for c in cars if c["car_id"] == car_id), None)
#     if not car:
#         return HTMLResponse("Машина не найдена", status_code=404)

#     return templates.TemplateResponse("edit_car.html", {"request": {}, "car": car})

# @app.post("/admin/cars/edit/{car_id}")
# def edit_car_submit(car_id: int, model: str = Form(...), description: str = Form(...), photo_url: str = Form(...)):
#     with open("cars.json", "r", encoding="utf-8") as f:
#         cars = json.load(f)

#     for car in cars:
#         if car["car_id"] == car_id:
#             car["model"] = model
#             car["description"] = description
#             car["photo_url"] = photo_url
#             break

#     with open("cars.json", "w", encoding="utf-8") as f:
#         json.dump(cars, f, indent=4, ensure_ascii=False)

#     return RedirectResponse(url="/admin/cars", status_code=303)

# @app.get("/admin/cars/add", response_class=HTMLResponse)
# def add_car_form(request: Request):
#     return templates.TemplateResponse("add_car.html", {"request": request})

# @app.post("/admin/cars/add")
# def add_car(model: str = Form(...), description: str = Form(...), photo_url: str = Form(...)):
#     with open("cars.json", "r", encoding="utf-8") as f:
#         cars = json.load(f)

#     # Новый car_id
#     if cars:
#         new_id = max(car["car_id"] for car in cars) + 1
#     else:
#         new_id = 1

#     new_car = {
#         "car_id": new_id,
#         "model": model,
#         "description": description,
#         "photo_url": photo_url,
#         "available": True
#     }
#     cars.append(new_car)

#     with open("cars.json", "w", encoding="utf-8") as f:
#         json.dump(cars, f, indent=4, ensure_ascii=False)

#     return RedirectResponse(url="/admin/cars", status_code=303)

# @app.post("/admin/cars/toggle/{car_id}")
# def toggle_car_availability(car_id: int):
#     with open("cars.json", "r", encoding="utf-8") as f:
#         cars = json.load(f)

#     for car in cars:
#         if car["car_id"] == car_id:
#             car["available"] = not car.get("available", True)
#             break

#     with open("cars.json", "w", encoding="utf-8") as f:
#         json.dump(cars, f, indent=4, ensure_ascii=False)

#     return RedirectResponse(url="/admin/cars", status_code=303)

# @app.get("/holidays")
# def get_holidays():
#     return HOLIDAYS

# BASE_DIR = pathlib.Path(__file__).parent.resolve()

# @app.get("/admin")
# async def admin_page(request: Request):
#     return templates.TemplateResponse("admin.html", {"request": request, "bookings": bookings})

# @app.post("/admin/delete/{booking_id}")
# async def delete_booking(booking_id: int):
#     global bookings
#     bookings = [b for b in bookings if b.get("booking_id") != booking_id]
#     save_bookings()
#     return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

# @app.get("/admin/edit/{booking_id}")
# def edit_booking_form(request: Request, booking_id: int):
#     bookings = load_bookings()
#     booking = next((b for b in bookings if b["booking_id"] == booking_id), None)
#     if not booking:
#         return HTMLResponse(content=f"<h3>Бронирование с ID {booking_id} не найдено</h3>", status_code=404)
    
#     # Загружаем список машин из cars.json
#     try:
#         with open("cars.json", "r", encoding="utf-8") as file:
#             cars = json.load(file)
#     except FileNotFoundError:
#         cars = []  # Если файла нет, используем пустой список
    
#     return templates.TemplateResponse("edit_booking.html", {
#         "request": request,
#         "booking": booking,
#         "cars": cars  # Теперь переменная определена
#     })

# @app.post("/admin/edit/{booking_id}")
# async def edit_booking(
#     booking_id: int,
#     request: Request,
#     car_id: str = Form(...),
#     user_name: str = Form(...),
#     model: str = Form(...),
#     booking_date: str = Form(...),
#     booking_start_time: str = Form(...),
#     booking_end_time: str = Form(...),
#     description: str = Form(...),
#     photo_url: str = Form(...)
# ):
#     try:
#         # Проверка на прошедшее время
#         booking_datetime = datetime.strptime(
#             f"{booking_date} {booking_start_time}", 
#             "%Y-%m-%d %H:%M"
#         )
#         if booking_datetime < datetime.now():
#             return templates.TemplateResponse(
#                 "edit_booking.html",
#                 {
#                     "request": request,
#                     "error": "Невозможно забронировать на прошедшее время",
#                     "booking": {
#                         "booking_id": booking_id,
#                         "car_id": car_id,
#                         "user_name": user_name,
#                         "model": model,
#                         "booking_date": booking_date,
#                         "booking_start_time": booking_start_time,
#                         "booking_end_time": booking_end_time,
#                         "description": description,
#                         "photo_url": photo_url
#                     },
#                     "cars": load_cars()
#                 },
#                 status_code=400
#             )
#     except ValueError:
#         pass  # Пропускаем ошибки парсинга даты (их обработают другие проверки)

#     # Остальная логика без изменений
#     try:
#         car_id_int = int(car_id)
#     except ValueError:
#         return {"error": "car_id должен быть числом"}
        
#     global bookings
#     load_bookings()
#     booking = next((b for b in bookings if b["booking_id"] == booking_id), None)
#     if not booking:
#         return HTMLResponse(content=f"<h3>Бронирование с ID {booking_id} не найдено</h3>", status_code=404)

#     # Обновляем данные бронирования
#     booking.update({
#         "user_name": user_name,
#         "model": model,
#         "car_id": car_id_int,
#         "description": description,
#         "photo_url": photo_url,
#         "booking_date": booking_date,
#         "booking_start_time": booking_start_time,
#         "booking_end_time": booking_end_time
#     })

#     save_bookings()

#     return RedirectResponse(url="/admin", status_code=303)

# @app.get("/")
# async def get_index():
#     index_path = BASE_DIR / "frontend" / "index.html"
#     with open(index_path, "r", encoding="utf-8") as f:
#         return HTMLResponse(content=f.read(), status_code=200)

# @app.get("/cars")
# async def get_cars():
#     cars = load_cars()
#     return {"cars": cars}


# class BookingRequest(BaseModel):
#     car_id: int
#     user_name: str
#     user_id: int
#     booking_date: str
#     booking_start_time: str
#     booking_end_time: str

# class CancelBookingRequest(BaseModel):
#     car_id: int
#     user_name: str
#     user_id: int
#     booking_date: str
#     booking_start_time: str
#     booking_end_time: str

# class UpdateBookingRequest(BaseModel):
#     old_car_id: int
#     old_date: str
#     old_start_time: str
#     old_end_time: str
#     new_car_id: int
#     new_date: str
#     new_start_time: str
#     new_end_time: str
#     user_id: int
#     user_name: str

# @app.post("/update_booking")
# async def update_booking(data: UpdateBookingRequest):
#     global next_booking_id  # используем глобальную переменную
#     global cars  # добавляем глобальную переменную cars

#     # 1. Проверяем существование cars
#     if 'cars' not in globals():
#         with open("cars.json", "r", encoding="utf-8") as f:
#             cars = json.load(f)  # загружаем данные о машинах

#     # 2. Отменяем старое бронирование (исправлено обращение к полям)
#     cancel_booking = next(
#         (b for b in bookings 
#          if b["user_id"] == data.user_id 
#          and b["car_id"] == data.old_car_id 
#          and b["booking_date"] == data.old_date
#          and b["booking_start_time"] == data.old_start_time
#          and b["booking_end_time"] == data.old_end_time),
#         None
#     )
    
#     if not cancel_booking:
#         raise HTTPException(status_code=404, detail="Старое бронирование не найдено")
    
#     bookings.remove(cancel_booking)
    
#     # 3. Создаем новое бронирование (с проверками)
#     new_booking = {
#         "booking_id": next_booking_id,
#         "car_id": data.new_car_id,
#         "user_name": data.user_name,
#         "user_id": data.user_id,
#         "booking_date": data.new_date,
#         "booking_start_time": data.new_start_time,
#         "booking_end_time": data.new_end_time
#     }

#     next_booking_id += 1
    
#     # Проверяем доступность нового слота
#     booking_start = datetime.strptime(f"{data.new_date} {data.new_start_time}", "%Y-%m-%d %H:%M")
#     booking_end = datetime.strptime(f"{data.new_date} {data.new_end_time}", "%Y-%m-%d %H:%M")
    
#     for b in bookings:
#         if b["car_id"] == data.new_car_id and b["booking_date"] == data.new_date:
#             existing_start = datetime.strptime(f"{b['booking_date']} {b['booking_start_time']}", "%Y-%m-%d %H:%M")
#             existing_end = datetime.strptime(f"{b['booking_date']} {b['booking_end_time']}", "%Y-%m-%d %H:%M")
            
#             if (booking_start < existing_end and booking_end > existing_start):
#                 raise HTTPException(
#                     status_code=400,
#                     detail="Машина уже забронирована в выбранный интервал времени."
#                 )
    
#     # 4. Добавляем данные машины (исправлено car["id"] на car["car_id"])
#     selected_car = next((car for car in cars if car["car_id"] == data.new_car_id), None)
#     if not selected_car:
#         raise HTTPException(status_code=404, detail="Машина не найдена")
    
#     new_booking.update({
#         "model": selected_car["model"],
#         "description": selected_car["description"],
#         "photo_url": selected_car["photo_url"]
#     })
    
#     # 5. Сохраняем изменения
#     bookings.append(new_booking)
#     save_bookings()  # убедитесь, что эта функция определена
    
#     return {"status": "success", "message": "Бронирование успешно обновлено"}

# @app.post("/choose_car")
# async def choose_car(data: BookingRequest):
#     global next_booking_id  # чтобы менять глобальную переменную

#     # ЗАГРУЗКА МАШИН ИЗ JSON
#     with open("cars.json", "r", encoding="utf-8") as f:
#         cars = json.load(f)

#     # --- Проверки ---
#     booking_date = datetime.strptime(data.booking_date, "%Y-%m-%d").date()
#     if booking_date.weekday() == 6 or data.booking_date in HOLIDAYS:
#         raise HTTPException(status_code=400, detail="Бронь в выходной день недоступна.")

#     if booking_date.weekday() == 5:
#         if data.booking_start_time < "10:00" or data.booking_end_time > "18:00":
#             raise HTTPException(status_code=400, detail="В субботу бронь доступна только с 10:00 до 18:00.")

#     if data.booking_start_time == "12:00" and data.booking_end_time == "13:00":
#         raise HTTPException(status_code=400, detail="Бронь на обеденный перерыв недоступна.")

#     user_bookings_count = sum(1 for b in bookings if b["user_id"] == data.user_id)
#     if user_bookings_count >= 3:
#         raise HTTPException(status_code=400, detail="Вы уже забронировали 3 машины. Отмените одну из них.")

#     booking_start = datetime.strptime(f"{data.booking_date} {data.booking_start_time}", "%Y-%m-%d %H:%M")
#     booking_end = datetime.strptime(f"{data.booking_date} {data.booking_end_time}", "%Y-%m-%d %H:%M")
#     if booking_start < datetime.now():
#         raise HTTPException(status_code=400, detail="Невозможно забронировать машину на прошедшее время.")
#     if booking_start >= booking_end:
#         raise HTTPException(status_code=400, detail="Время начала бронирования должно быть раньше времени окончания.")

#     for b in bookings:
#         if b["car_id"] == data.car_id and b["booking_date"] == data.booking_date:
#             existing_start = datetime.strptime(f"{b['booking_date']} {b['booking_start_time']}", "%Y-%m-%d %H:%M")
#             existing_end = datetime.strptime(f"{b['booking_date']} {b['booking_end_time']}", "%Y-%m-%d %H:%M")
#             if booking_start < existing_end and booking_end > existing_start:
#                 raise HTTPException(status_code=400, detail="Машина уже забронирована в выбранный интервал времени.")

#     # Поиск машины
#     selected_car = next((car for car in cars if car["car_id"] == data.car_id), None)

#     if not selected_car:
#         raise HTTPException(status_code=404, detail="Машина не найдена.")

#     new_booking = {
#         "booking_id": next_booking_id,
#         "car_id": data.car_id,
#         "user_name": data.user_name,
#         "user_id": data.user_id,
#         "model": selected_car["model"],
#         "description": selected_car["description"],
#         "photo_url": selected_car["photo_url"],
#         "booking_date": data.booking_date,
#         "booking_start_time": data.booking_start_time,
#         "booking_end_time": data.booking_end_time
#     }

#     bookings.append(new_booking)
#     next_booking_id += 1
#     save_bookings()

#     return {
#         "status": "success",
#         "message": f"{selected_car['model']} забронирована на {data.booking_date} с {data.booking_start_time} до {data.booking_end_time}!"
#     }


# @app.post("/cancel_booking")
# async def cancel_booking(data: CancelBookingRequest):
#     booking = next(
#         (b for b in bookings 
#          if b["user_id"] == data.user_id 
#          and b["car_id"] == data.car_id 
#          and b["booking_date"] == data.booking_date
#          and b["booking_start_time"] == data.booking_start_time),
#         None
#     )

#     if booking:
#         bookings.remove(booking)
#         save_bookings()
#         return {
#             "status": "success",
#             "message": f"Бронирование на {data.booking_date} с {data.booking_start_time} отменено."
#         }

#     raise HTTPException(status_code=404, detail="Бронирование не найдено.")

# @app.get("/my_bookings")
# async def get_bookings(user_id: int = Query(...)):
#     user_bookings = [
#         {
#             "car_id": b["car_id"],
#             "model": b["model"],
#             "description": b["description"],
#             "photo_url": b["photo_url"],
#             "booking_date": b["booking_date"],
#             "booking_start_time": b["booking_start_time"],
#             "booking_end_time": b["booking_end_time"]
#         }
#         for b in bookings if b["user_id"] == user_id
#     ]
    
#     return {"status": "success", "bookings": user_bookings} if user_bookings else {"status": "error", "message": "Нет активных бронирований"}

# @app.get("/car_bookings")
# async def get_car_bookings(car_id: int = Query(...), date: str = Query(None)):
#     """Возвращает все бронирования для указанной машины (опционально - на конкретную дату)"""
#     car_bookings = []
#     for booking in bookings:
#         if booking["car_id"] == car_id:
#             if date is None or booking["booking_date"] == date:
#                 car_bookings.append({
#                     "booking_date": booking["booking_date"],
#                     "booking_start_time": booking["booking_start_time"],
#                     "booking_end_time": booking["booking_end_time"]
#                 })
    
#     return car_bookings

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Query
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from datetime import datetime
from fastapi.responses import RedirectResponse
from fastapi import status
from pathlib import Path
import pathlib
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

bookings = []
BOOKINGS_FILE = "bookings.json"
CARS_FILE = "cars.json"
HOLIDAYS = ["2025-01-01",
"2025-01-02",
"2025-01-03", 
"2025-01-04", 
"2025-01-06", 
"2025-01-07",
"2025-01-08", 
"2025-03-08", 
"2025-05-01",
"2025-05-02",
"2025-05-03",
"2025-05-08",
"2025-05-09",
"2025-05-10",
"2025-06-12",
"2025-06-13",
"2025-06-14",
"2025-11-03",
"2025-11-04",
"2025-12-31"
]

next_booking_id = 1

def load_bookings():
    global next_booking_id
    bookings.clear()  # очищаем глобальный список
    max_id = 0
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
            loaded_bookings = json.load(f)
            for b in loaded_bookings:
                if "booking_id" not in b:
                    b["booking_id"] = next_booking_id
                    next_booking_id += 1
                else:
                    if b["booking_id"] > max_id:
                        max_id = b["booking_id"]
                bookings.append(b)
            if max_id >= next_booking_id:
                next_booking_id = max_id + 1
    return bookings

def save_bookings():
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, ensure_ascii=False, indent=4)

load_bookings()



def load_cars():
    if not os.path.exists(CARS_FILE):
        return []
    with open(CARS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/admin/cars", response_class=HTMLResponse)
def view_cars(request: Request):
    cars = load_cars()
    return templates.TemplateResponse("admin_cars.html", {"request": request, "cars": cars})

@app.post("/admin/cars/delete/{car_id}")
def delete_car(car_id: int):
    with open("cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    new_cars = [car for car in cars if car["car_id"] != car_id]

    with open("cars.json", "w", encoding="utf-8") as f:
        json.dump(new_cars, f, indent=4, ensure_ascii=False)

    return RedirectResponse(url="/admin/cars", status_code=303)

@app.get("/admin/cars/edit/{car_id}", response_class=HTMLResponse)
def edit_car_form(car_id: int):
    with open("cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    car = next((c for c in cars if c["car_id"] == car_id), None)
    if not car:
        return HTMLResponse("инструктор не найден", status_code=404)

    return templates.TemplateResponse("edit_car.html", {"request": {}, "car": car})

@app.post("/admin/cars/edit/{car_id}")
def edit_car_submit(car_id: int, model: str = Form(...), description: str = Form(...), photo_url: str = Form(...)):
    with open("cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    for car in cars:
        if car["car_id"] == car_id:
            car["model"] = model
            car["description"] = description
            car["photo_url"] = photo_url
            break

    with open("cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4, ensure_ascii=False)

    return RedirectResponse(url="/admin/cars", status_code=303)

@app.get("/admin/cars/add", response_class=HTMLResponse)
def add_car_form(request: Request):
    return templates.TemplateResponse("add_car.html", {"request": request})

@app.post("/admin/cars/add")
def add_car(model: str = Form(...), description: str = Form(...), photo_url: str = Form(...)):
    with open("cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    # Новый car_id
    if cars:
        new_id = max(car["car_id"] for car in cars) + 1
    else:
        new_id = 1

    new_car = {
        "car_id": new_id,
        "model": model,
        "description": description,
        "photo_url": photo_url,
        "available": True
    }

    cars.append(new_car)

    with open("cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4, ensure_ascii=False)

    return RedirectResponse(url="/admin/cars", status_code=303)

@app.post("/admin/cars/toggle/{car_id}")
def toggle_car_availability(car_id: int):
    with open("cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    for car in cars:
        if car["car_id"] == car_id:
            car["available"] = not car.get("available", True)
            break

    with open("cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4, ensure_ascii=False)

    return RedirectResponse(url="/admin/cars", status_code=303)

@app.get("/holidays")
def get_holidays():
    return HOLIDAYS

BASE_DIR = pathlib.Path(__file__).parent.resolve()

@app.get("/admin")
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request, "bookings": bookings})

@app.post("/admin/delete/{booking_id}")
async def delete_booking(booking_id: int):
    global bookings
    bookings = [b for b in bookings if b.get("booking_id") != booking_id]
    save_bookings()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/admin/edit/{booking_id}")
def edit_booking_form(request: Request, booking_id: int):
    bookings = load_bookings()
    booking = next((b for b in bookings if b["booking_id"] == booking_id), None)
    if not booking:
        return HTMLResponse(content=f"<h3>Бронирование с ID {booking_id} не найдено</h3>", status_code=404)
    
    # Загружаем список машин из cars.json
    try:
        with open("cars.json", "r", encoding="utf-8") as file:
            cars = json.load(file)
    except FileNotFoundError:
        cars = []  # Если файла нет, используем пустой список
    
    return templates.TemplateResponse("edit_booking.html", {
        "request": request,
        "booking": booking,
        "cars": cars  # Теперь переменная определена
    })

@app.post("/admin/edit/{booking_id}")
async def edit_booking(
    booking_id: int,
    request: Request,
    car_id: str = Form(...),
    user_name: str = Form(...),
    model: str = Form(...),
    booking_date: str = Form(...),
    booking_start_time: str = Form(...),
    booking_end_time: str = Form(...),
    description: str = Form(...),
    photo_url: str = Form(...)
):
    try:
        # Проверка на прошедшее время
        booking_datetime = datetime.strptime(
            f"{booking_date} {booking_start_time}", 
            "%Y-%m-%d %H:%M"
        )
        if booking_datetime < datetime.now():
            return templates.TemplateResponse(
                "edit_booking.html",
                {
                    "request": request,
                    "error": "Невозможно забронировать на прошедшее время",
                    "booking": {
                        "booking_id": booking_id,
                        "car_id": car_id,
                        "user_name": user_name,
                        "model": model,
                        "booking_date": booking_date,
                        "booking_start_time": booking_start_time,
                        "booking_end_time": booking_end_time,
                        "description": description,
                        "photo_url": photo_url
                    },
                    "cars": load_cars()
                },
                status_code=400
            )
    except ValueError:
        pass  # Пропускаем ошибки парсинга даты (их обработают другие проверки)

    # Остальная логика без изменений
    try:
        car_id_int = int(car_id)
    except ValueError:
        return {"error": "car_id должен быть числом"}
        
    global bookings
    load_bookings()
    booking = next((b for b in bookings if b["booking_id"] == booking_id), None)
    if not booking:
        return HTMLResponse(content=f"<h3>Бронирование с ID {booking_id} не найдено</h3>", status_code=404)

    # Обновляем данные бронирования
    booking.update({
        "user_name": user_name,
        "model": model,
        "car_id": car_id_int,
        "description": description,
        "photo_url": photo_url,
        "booking_date": booking_date,
        "booking_start_time": booking_start_time,
        "booking_end_time": booking_end_time
    })

    save_bookings()

    return RedirectResponse(url="/admin", status_code=303)

@app.get("/")
async def get_index():
    index_path = BASE_DIR / "frontend" / "index.html"
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/cars")
async def get_cars():
    cars = load_cars()
    return {"cars": cars}

class BookingRequest(BaseModel):
    car_id: int
    user_name: str
    user_id: int
    booking_date: str
    booking_start_time: str
    booking_end_time: str

class CancelBookingRequest(BaseModel):
    car_id: int
    user_name: str
    user_id: int
    booking_date: str
    booking_start_time: str
    booking_end_time: str

class UpdateBookingRequest(BaseModel):
    old_car_id: int
    old_date: str
    old_start_time: str
    old_end_time: str
    new_car_id: int
    new_date: str
    new_start_time: str
    new_end_time: str
    user_id: int
    user_name: str

@app.post("/update_booking")
async def update_booking(data: UpdateBookingRequest):
    global next_booking_id  # используем глобальную переменную
    global cars  # добавляем глобальную переменную cars

    # 1. Проверяем существование cars
    if 'cars' not in globals():
        with open("cars.json", "r", encoding="utf-8") as f:
            cars = json.load(f)  # загружаем данные о машинах

    # 2. Отменяем старое бронирование (исправлено обращение к полям)
    cancel_booking = next(
        (b for b in bookings 
         if b["user_id"] == data.user_id 
         and b["car_id"] == data.old_car_id 
         and b["booking_date"] == data.old_date
         and b["booking_start_time"] == data.old_start_time
         and b["booking_end_time"] == data.old_end_time),
        None
    )
    
    if not cancel_booking:
        raise HTTPException(status_code=404, detail="Старое бронирование не найдено")
    
    bookings.remove(cancel_booking)
    
    # 3. Создаем новое бронирование (с проверками)
    new_booking = {
        "booking_id": next_booking_id,
        "car_id": data.new_car_id,
        "user_name": data.user_name,
        "user_id": data.user_id,
        "booking_date": data.new_date,
        "booking_start_time": data.new_start_time,
        "booking_end_time": data.new_end_time
    }

    next_booking_id += 1
    
    # Проверяем доступность нового слота
    booking_start = datetime.strptime(f"{data.new_date} {data.new_start_time}", "%Y-%m-%d %H:%M")
    booking_end = datetime.strptime(f"{data.new_date} {data.new_end_time}", "%Y-%m-%d %H:%M")
    
    for b in bookings:
        if b["car_id"] == data.new_car_id and b["booking_date"] == data.new_date:
            existing_start = datetime.strptime(f"{b['booking_date']} {b['booking_start_time']}", "%Y-%m-%d %H:%M")
            existing_end = datetime.strptime(f"{b['booking_date']} {b['booking_end_time']}", "%Y-%m-%d %H:%M")
            
            if (booking_start < existing_end and booking_end > existing_start):
                raise HTTPException(
                    status_code=400,
                    detail="Инструктор уже забронирован в выбранный интервал времени."
                )
    
    # 4. Добавляем данные машины (исправлено car["id"] на car["car_id"])
    selected_car = next((car for car in cars if car["car_id"] == data.new_car_id), None)
    if not selected_car:
        raise HTTPException(status_code=404, detail="Инструктор не найден")
    
    new_booking.update({
        "model": selected_car["model"],
        "description": selected_car["description"],
        "photo_url": selected_car["photo_url"]
    })
    
    # 5. Сохраняем изменения
    bookings.append(new_booking)
    save_bookings()  # убедитесь, что эта функция определена
    
    return {"status": "success", "message": "Бронирование успешно обновлено"}

@app.post("/choose_car")
async def choose_car(data: BookingRequest):
    global next_booking_id  # чтобы менять глобальную переменную

    # ЗАГРУЗКА МАШИН ИЗ JSON
    with open("cars.json", "r", encoding="utf-8") as f:
        cars = json.load(f)

    # --- Проверки ---
    booking_date = datetime.strptime(data.booking_date, "%Y-%m-%d").date()
    if booking_date.weekday() == 6 or data.booking_date in HOLIDAYS:
        raise HTTPException(status_code=400, detail="Бронь в выходной день недоступна.")

    if booking_date.weekday() == 5:
        if data.booking_start_time < "10:00" or data.booking_end_time > "18:00":
            raise HTTPException(status_code=400, detail="В субботу бронь доступна только с 10:00 до 18:00.")

    if data.booking_start_time == "12:00" and data.booking_end_time == "13:00":
        raise HTTPException(status_code=400, detail="Бронь на обеденный перерыв недоступна.")

    user_bookings_count = sum(1 for b in bookings if b["user_id"] == data.user_id)
    if user_bookings_count >= 3:
        raise HTTPException(status_code=400, detail="Вы уже забронировали 3 инструкторов. Отмените одно из бронирований.")

    booking_start = datetime.strptime(f"{data.booking_date} {data.booking_start_time}", "%Y-%m-%d %H:%M")
    booking_end = datetime.strptime(f"{data.booking_date} {data.booking_end_time}", "%Y-%m-%d %H:%M")
    if booking_start < datetime.now():
        raise HTTPException(status_code=400, detail="Невозможно забронировать инструктора на прошедшее время.")
    if booking_start >= booking_end:
        raise HTTPException(status_code=400, detail="Время начала бронирования должно быть раньше времени окончания.")

    for b in bookings:
        if b["car_id"] == data.car_id and b["booking_date"] == data.booking_date:
            existing_start = datetime.strptime(f"{b['booking_date']} {b['booking_start_time']}", "%Y-%m-%d %H:%M")
            existing_end = datetime.strptime(f"{b['booking_date']} {b['booking_end_time']}", "%Y-%m-%d %H:%M")
            if booking_start < existing_end and booking_end > existing_start:
                raise HTTPException(status_code=400, detail="инструктор уже забронирован в выбранный интервал времени.")

    # Поиск машины
    selected_car = next((car for car in cars if car["car_id"] == data.car_id), None)

    if not selected_car:
        raise HTTPException(status_code=404, detail="Инструктор не найден.")

    new_booking = {
        "booking_id": next_booking_id,
        "car_id": data.car_id,
        "user_name": data.user_name,
        "user_id": data.user_id,
        "model": selected_car["model"],
        "description": selected_car["description"],
        "photo_url": selected_car["photo_url"],
        "booking_date": data.booking_date,
        "booking_start_time": data.booking_start_time,
        "booking_end_time": data.booking_end_time
    }

    bookings.append(new_booking)
    next_booking_id += 1
    save_bookings()

    return {
        "status": "success",
        "message": f"{selected_car['model']} забронирован на {data.booking_date} с {data.booking_start_time} до {data.booking_end_time}!"
    }


@app.post("/cancel_booking")
async def cancel_booking(data: CancelBookingRequest):
    booking = next(
        (b for b in bookings 
         if b["user_id"] == data.user_id 
         and b["car_id"] == data.car_id 
         and b["booking_date"] == data.booking_date
         and b["booking_start_time"] == data.booking_start_time),
        None
    )

    if booking:
        bookings.remove(booking)
        save_bookings()
        return {
            "status": "success",
            "message": f"Бронирование на {data.booking_date} с {data.booking_start_time} отменено."
        }

    raise HTTPException(status_code=404, detail="Бронирование не найдено.")

@app.get("/my_bookings")
async def get_bookings(user_id: int = Query(...)):
    user_bookings = [
        {
            "car_id": b["car_id"],
            "model": b["model"],
            "description": b["description"],
            "photo_url": b["photo_url"],
            "booking_date": b["booking_date"],
            "booking_start_time": b["booking_start_time"],
            "booking_end_time": b["booking_end_time"]
        }
        for b in bookings if b["user_id"] == user_id
    ]
    
    return {"status": "success", "bookings": user_bookings} if user_bookings else {"status": "error", "message": "Нет активных бронирований"}

@app.get("/car_bookings")
async def get_car_bookings(car_id: int = Query(...), date: str = Query(None)):
    """Возвращает все бронирования для указанного инструктора (опционально - на конкретную дату)"""
    car_bookings = []
    for booking in bookings:
        if booking["car_id"] == car_id:
            if date is None or booking["booking_date"] == date:
                car_bookings.append({
                    "booking_date": booking["booking_date"],
                    "booking_start_time": booking["booking_start_time"],
                    "booking_end_time": booking["booking_end_time"]
                })
    
    return car_bookings
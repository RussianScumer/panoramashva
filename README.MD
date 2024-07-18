# Обработанный шов:

## key_framesver13.py 

## key_framesver15.py 


# Все необходимые переменные


## video_path (str)
### название видео без .mp4
## saved_img_name  (str)
## название сохраннённого изображения
## size_of_frames  (int)
### то какую часть в последующем будем брать из видео
## auto  (bool)
### замер скорости изоленты, если True, замеряет скорость автоматически по СИНЕЙ изленте в видео  если False, необходимо рассчиать videothresh вручную
## videothresh (int)  
### частота кадров, через которую берем их из видео из расчёта 30 кадров в секунду 30*время смены кадра / size_of_frames
# 
## framecount (int)  
### задержка, чтобы пропустить остановку и т.п (-150  это простой камеры в кадрах 30*sec )


# Необработанный шов

## stitcher_unprocessed.py

# Все необходимые переменные


## how_to_stitch (bool)
### Сшивать либо до конца алгоритмами, либо последний шаг втупую, зависит от качества видео, тряски и т.п.
## vid_name  
### Здесь название видео, которое надо разбить на кадры
## step (int)
### Начальный шаг
## overlap (int)  
### Перехлёст количества фото
## num_to_stich (int)  
### Количество склеиваемых фото. Чем больше, тем квадратично дольше ждать и менее стабильно. 10

# Остальные посянения закоментированы и есть в коде
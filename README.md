## 꿀팁

1. np.qunique
  unique, count = (np.unique(VARIABLE, return_counts=True))
  uniq_count = dict(zip(unique, count))

2. np.all
  - rgb channel에서 특정 pixel 값을 찾을 때
  black_pixels_mask = np.all(image == [0, 0, 0], axis=-1)
  
3. np.count_nonzero
  count = np.count_nonzero(black_pixels_mask == True)



### black color object
  찾는 방법
  cv2.cvtColor(garyscale) -> cv2.threshold(cv2.THRESH_BINARY) -> threshold(특정 수치이상)

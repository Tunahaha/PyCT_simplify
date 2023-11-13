import test_dnnct_cnn 
import test_dnnct_tnn

import random


# # set the seed
# random.seed(42)


# def random_pixel(n):
#     # create an empty list to store the pixels
#     pixels = []
#     for _ in range(n):
#         # generate a random integer between 0 and 72
#         i = random.randint(0, 72)
#         j = random.randint(0, 72)
    
#         # create the string
#         pixel = f"v_{i}_{j}_0"
    
#         # add the pixel to the list
#         pixels.append(pixel)
   
#     return pixels



# def one_pixel_test():
#     cnn_count, tnn_count = 0, 0
#     pixels=random_pixel(64)

#     for i in pixels:
#         cnn_count=cnn_count+test_dnnct_cnn.one_pixel_test(6,i)
#         tnn_count=tnn_count+test_dnnct_tnn.one_pixel_test(6,i)
#     print("cnn_count:",cnn_count)
#     print("tnn_count:",tnn_count)

# def eight_pixel_test():
#     cnn_count, tnn_count = 0, 0
#     for i in range(4):
#         pixels=random_pixel(32)
#         cnn_count=cnn_count+test_dnnct_cnn.eight_pixel_test(i,6,pixels)
#         tnn_count=tnn_count+test_dnnct_tnn.eight_pixel_test(i,6,pixels)
#     with open(f'out/{len(pixels)}cnn_rate.txt', 'w') as file:
#         file.write('cnn_count: {} '.format(cnn_count))
#     with open(f'out/{len(pixels)}tnn_rate.txt', 'w') as file:
#         file.write('tnn_count: {} '.format(tnn_count))
#     print("cnn_count:",cnn_count)
#     print("tnn_count:",tnn_count)
# def sixty_pixel_test():
#     cnn_count, tnn_count = 0, 0
#     for i in range():
#         pixels=random_pixel(16)
#         cnn_count=cnn_count+test_dnnct_cnn.eight_pixel_test(i,6,pixels)
#         tnn_count=tnn_count+test_dnnct_tnn.eight_pixel_test(i,6,pixels)
#     with open(f'out/{len(pixels)}cnn_rate.txt', 'w') as file:
#         file.write('cnn_count: {} '.format(cnn_count))
#     with open(f'out/{len(pixels)}tnn_rate.txt', 'w') as file:
#         file.write('tnn_count: {} '.format(tnn_count))
#     print("cnn_count:",cnn_count)
#     print("tnn_count:",tnn_count)
eight_pixel_test()
from pylab import *
import numpy as np
import matplotlib.pyplot as plt

#Precision_Recall_Graph
plot([0.0119,0.0091,0.0075,0.0065,0.0051,0.0023,0.0014,0.0006,0.0003],[0.0597,0.0907,0.1124,0.1292,0.1545,0.2298,0.2721,0.3175,0.3493], label="VSM_MultiFieldsSearch")
plot([0.0048,0.0039,0.0034,0.0031,0.0026,0.0015,0.0011,0.0006,0.0004],[0.0238,0.0393,0.0511,0.061,0.0778,0.1496,0.211,0.3104,0.4016], label="VSM_SimpleSearch")
plot([0.0384,0.0244,0.0184,0.015,0.011,0.0042,0.0024,0.0011,0.0006],[0.1921,0.2438,0.2756,0.2996,0.3312,0.4231,0.4737,0.5415,0.5946], label="BM25_MultiFieldsSearch")
plot([0.0499,0.0311,0.0233,0.0188,0.0138,0.0052,0.0029,0.0013,0.0007],[0.2496,0.3115,0.3492,0.3763,0.4137,0.524,0.5834,0.656,0.7063], label="BM25_SimpleSearch")
ylabel('Recall')
xlabel('Precision')
legend()
show()


# # MRR_Histogram
# height = [0.0190, 0.0404, 0.1865, 0.1424]
# bars = ('VSM_SimpleSearch', 'VSM_MultiFieldsSearch', 'BM25_SimpleSearch', 'BM25_MultiFieldsSearch')
# y_pos = np.arange(len(bars))
# plt.bar(y_pos, height, color = (0.8,0.10,0.2 ))
# plt.ylabel('Mean Reciprocal Rank (MRR) ')
# plt.ylim(0,0.3)
# plt.xticks(y_pos, bars)
# plt.show()

# #MAP_Histogram
# height = [0.0190, 0.0404, 0.1865, 0.1424]
# bars = ('VSM_SimpleSearch', 'VSM_MultiFieldsSearch', 'BM25_SimpleSearch', 'BM25_MultiFieldsSearch')
# y_pos = np.arange(len(bars))
# plt.bar(y_pos, height, color = (0,0.1,0.4 ))
# plt.ylabel('Mean Average Precision (MAP) ')
# plt.ylim(0,0.3)
# plt.xticks(y_pos, bars)
# plt.show()

# # R_Pre_Histogram
# height = [0.0071, 0.0159, 0.1236, 0.0917]
# bars = ('VSM_SimpleSearch', 'VSM_MultiFieldsSearch', 'BM25_SimpleSearch','BM25_MultiFieldsSearch')
# y_pos = np.arange(len(bars))
# plt.bar(y_pos, height, color = (0,0.6,0.4))
# plt.ylabel('R-Precision (R-Prec) ')
# plt.ylim(0,0.3)
# plt.xticks(y_pos, bars)
# plt.show()

# #R@K Graph
# 
# plot([5,10,15,20,30,100,200,500,1000],[0.0597,0.0907,0.1124,0.1292,0.1545,0.2298,0.2721,0.3175,0.3493], label="VSM_MultiFieldsSearch")
# plot([5,10,15,20,30,100,200,500,1000],[0.0238,0.0393,0.0511,0.061,0.0778,0.1496,0.211,0.3104,0.4016], label="VSM_SimpleSearch")
# plot([5,10,15,20,30,100,200,500,1000],[0.1921,0.2438,0.2756,0.2996,0.3312,0.4231,0.4737,0.5415,0.5946], label="BM25_MultiFieldsSearch")
# plot([5,10,15,20,30,100,200,500,1000],[0.2496,0.3115,0.3492,0.3763,0.4137,0.524,0.5834,0.656,0.7063], label="BM25_SimpleSearch")
# ylabel('R@K')
# xlabel('K')
# legend()
# show()

# #P@K Graph
# plot([5,10,15,20,30,100,200,500,1000],[0.0119,0.0091,0.0075,0.0065,0.0051,0.0023,0.0014,0.0006,0.0003], label="VSM_MultiFieldsSearch")
# plot([5,10,15,20,30,100,200,500,1000],[0.0048,0.0039,0.0034,0.0031,0.0026,0.0015,0.0011,0.0006,0.0004], label="VSM_SimpleSearch")
# plot([5,10,15,20,30,100,200,500,1000],[0.0384,0.0244,0.0184,0.015,0.011,0.0042,0.0024,0.0011,0.0006], label="BM25_MultiFieldsSearch")
# plot([5,10,15,20,30,100,200,500,1000],[0.0499,0.0311,0.0233,0.0188,0.0138,0.0052,0.0029,0.0013,0.0007], label="BM25_SimpleSearch")
# ylabel('P@K')
# xlabel('K')
# legend()
# show()




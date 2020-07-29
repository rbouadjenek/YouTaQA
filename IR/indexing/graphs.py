from pylab import *
import numpy as np
import matplotlib.pyplot as plt

# Precision_Recall_Graph
plot([0.0225,0.0164,0.0132,0.0113,0.0088,0.0039,0.0024,0.0012,0.0007],[0.1126,0.1641,0.1981,0.225,0.2651,0.3922,0.4716,0.5757,0.6532], label="VSM_MultiFieldsSearch_Question+TitleAsQuery")
plot([0.0119,0.0091,0.0075,0.0065,0.0051,0.0023,0.0014,0.0006,0.0003],[0.0597,0.0907,0.1124,0.1292,0.1545,0.2298,0.2721,0.3175,0.3493], label="VSM_MultiFieldsSearch_QuestionAsQuery")
plot([0.0296,0.0208,0.0166,0.014,0.0109,0.0048,0.0029,0.0014,0.0008],[0.1478,0.2084,0.2487,0.2795,0.326,0.4802,0.5728,0.6913,0.7688], label="VSM_SimpleSearch_Question+TitleAsQuery")
plot([0.0048,0.0039,0.0034,0.0031,0.0026,0.0015,0.0011,0.0006,0.0004],[0.0238,0.0393,0.0511,0.061,0.0778,0.1496,0.211,0.3104,0.4016], label="VSM_SimpleSearch_QuestionAsQuery")
plot([0.0541,0.0351,0.0267,0.0218,0.0161,0.0062,0.0035,0.0016,0.0008],[0.2704,0.3514,0.4004,0.4355,0.4844,0.6223,0.6938,0.7775,0.8314], label="BM25_MultiFieldsSearch_Question+TitleAsQuery")
plot([0.0384,0.0244,0.0184,0.015,0.011,0.0042,0.0024,0.0011,0.0006],[0.1921,0.2438,0.2756,0.2996,0.3312,0.4231,0.4737,0.5415,0.5946], label="BM25_MultiFieldsSearch_QuestionAsQuery")
plot([0.0697,0.0432,0.032,0.0257,0.0186,0.0068,0.0037,0.0016,0.0008],[0.3487,0.4319,0.4799,0.5139,0.5593,0.6806,0.7418,0.8089,0.8493], label="BM25_SimpleSearch_Question+TitleAsQuery")
plot([0.0499,0.0311,0.0233,0.0188,0.0138,0.0052,0.0029,0.0013,0.0007],[0.2496,0.3115,0.3492,0.3763,0.4137,0.524,0.5834,0.656,0.7063], label="BM25_SimpleSearch_QuestionAsQuery")
ylabel('Recall')
xlabel('Precision')
legend()
show()


# # MRR_Histogram
# height = [0.0190, 0.1062, 0.0778, 0.0404, 0.1865, 0.1982, 0.1424, 0.2596]
# bars = ('VSM_SS_QQ', 'VSM_SS_QTQ', 'VSM_MFS_QTQ', 'VSM_MFS_QQ', 'BM25_SS_QQ', 'BM25_MFS_QTQ', 'BM25_MFS_QQ','BM25_SS_QTQ')
# y_pos = np.arange(len(bars))
# plt.bar(y_pos, height, color = (0.8,0.10,0.2 ))
# plt.ylabel('Mean Reciprocal Rank (MRR) ')
# plt.ylim(0,0.3)
# plt.xticks(y_pos, bars)
# plt.show()

# #MAP_Histogram
# height = [0.0190, 0.1062, 0.0778, 0.0404, 0.1865, 0.1982, 0.1424, 0.2596]
# bars = ('VSM_SS_QQ', 'VSM_SS_QTQ', 'VSM_MFS_QTQ', 'VSM_MFS_QQ', 'BM25_SS_QQ', 'BM25_MFS_QTQ', 'BM25_MFS_QQ','BM25_SS_QTQ')
# y_pos = np.arange(len(bars))
# plt.bar(y_pos, height, color = (0,0.1,0.4 ))
# plt.ylabel('Mean Average Precision (MAP) ')
# plt.ylim(0,0.3)
# plt.xticks(y_pos, bars)
# plt.show()

# # R_Pre_Histogram
# height = [0.0071, 0.0548, 0.0346, 0.0159, 0.1236, 0.1237, 0.0917, 0.1738]
# bars = ('VSM_SS_QQ', 'VSM_SS_QTQ', 'VSM_MFS_QTQ', 'VSM_MFS_QQ', 'BM25_SS_QQ', 'BM25_MFS_QTQ', 'BM25_MFS_QQ','BM25_SS_QTQ')
# y_pos = np.arange(len(bars))
# plt.bar(y_pos, height, color = (0,0.6,0.4))
# plt.ylabel('R-Precision (R-Prec) ')
# plt.ylim(0,0.3)
# plt.xticks(y_pos, bars)
# plt.show()

# #R@K Graph
# plot([5,10,15,20,30,100,200,500,1000],[0.1126,0.1641,0.1981,0.225,0.2651,0.3922,0.4716,0.5757,0.6532], label="VSM_MultiFieldsSearch_Question+TitleAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0597,0.0907,0.1124,0.1292,0.1545,0.2298,0.2721,0.3175,0.3493], label="VSM_MultiFieldsSearch_QuestionAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.1478,0.2084,0.2487,0.2795,0.326,0.4802,0.5728,0.6913,0.7688], label="VSM_SimpleSearch_Question+TitleAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0238,0.0393,0.0511,0.061,0.0778,0.1496,0.211,0.3104,0.4016], label="VSM_SimpleSearch_QuestionAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.2704,0.3514,0.4004,0.4355,0.4844,0.6223,0.6938,0.7775,0.8314], label="BM25_MultiFieldsSearch_Question+TitleAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.1921,0.2438,0.2756,0.2996,0.3312,0.4231,0.4737,0.5415,0.5946], label="BM25_MultiFieldsSearch_QuestionAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.3487,0.4319,0.4799,0.5139,0.5593,0.6806,0.7418,0.8089,0.8493], label="BM25_SimpleSearch_Question+TitleAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.2496,0.3115,0.3492,0.3763,0.4137,0.524,0.5834,0.656,0.7063], label="BM25_SimpleSearch_QuestionAsQuery")
# ylabel('R@K')
# xlabel('K')
# legend()
# show()

# #P@K Graph
# plot([5,10,15,20,30,100,200,500,1000],[0.0225,0.0164,0.0132,0.0113,0.0088,0.0039,0.0024,0.0012,0.0007], label="VSM_MultiFieldsSearch_Question+TitleAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0119,0.0091,0.0075,0.0065,0.0051,0.0023,0.0014,0.0006,0.0003], label="VSM_MultiFieldsSearch_QuestionAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0296,0.0208,0.0166,0.014,0.0109,0.0048,0.0029,0.0014,0.0008], label="VSM_SimpleSearch_Question+TitleAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0048,0.0039,0.0034,0.0031,0.0026,0.0015,0.0011,0.0006,0.0004], label="VSM_SimpleSearch_QuestionAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0541,0.0351,0.0267,0.0218,0.0161,0.0062,0.0035,0.0016,0.0008], label="BM25_MultiFieldsSearch_Question+TitleAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0384,0.0244,0.0184,0.015,0.011,0.0042,0.0024,0.0011,0.0006], label="BM25_MultiFieldsSearch_QuestionAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0697,0.0432,0.032,0.0257,0.0186,0.0068,0.0037,0.0016,0.0008], label="BM25_SimpleSearch_Question+TitleAsQuery")
# plot([5,10,15,20,30,100,200,500,1000],[0.0499,0.0311,0.0233,0.0188,0.0138,0.0052,0.0029,0.0013,0.0007], label="BM25_SimpleSearch_QuestionAsQuery")
# ylabel('P@K')
# xlabel('K')
# legend()
# show()




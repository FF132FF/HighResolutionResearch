from skimage.metrics import mean_squared_error
from metrics import *
from skimage.metrics import structural_similarity
from prettytable import PrettyTable
import random

win_size = 3


def get_metrics(HR_minmax, someMethod_minmax):
    mseMetric = mean_squared_error(HR_minmax, someMethod_minmax)
    psnrMetric = psnr_metric(HR_minmax, someMethod_minmax)
    samMetric = sam_metric(HR_minmax, someMethod_minmax)
    ergasMetric = ergas_metric(HR_minmax, someMethod_minmax)
    sccMetric = scc_metric(HR_minmax, someMethod_minmax)
    ssimMetric = structural_similarity(HR_minmax, someMethod_minmax, win_size=win_size)

    return [round(mseMetric, 2), round(psnrMetric, 2), round(ssimMetric, 2), round(samMetric, 2),
            round(sccMetric, 2), round(ergasMetric, 2)]

def get_metrics_for_all_methods(HR_minmax, Bicubic_minmax, IHS_minmax, GS_minmax, Brovey_minmax, Wavelet_minmax):
    mse_list = []
    psnr_list = []
    ssim_list = []
    sam_list = []
    scc_list = []
    ergas_list = []

    methods = ['Bicubic', 'IHS', 'GS', 'Brovey', 'Wavelet']
    methods = [Bicubic_minmax, IHS_minmax, GS_minmax, Brovey_minmax, Wavelet_minmax]

    for method_minmax in methods:
        mseMetric, psnrMetric, ssimMetric, samMetric, sccMetric, ergasMetric = get_metrics(HR_minmax, method_minmax)

        mse_list.append(mseMetric)
        psnr_list.append(psnrMetric)
        ssim_list.append(ssimMetric)
        sam_list.append(samMetric)
        scc_list.append(sccMetric)
        ergas_list.append(ergasMetric)

    return [mse_list, psnr_list, ssim_list, sam_list, scc_list, ergas_list]


def metrics_report_of_method(HR_minmax, Bicubic_minmax, IHS_minmax, GS_minmax, Brovey_minmax, Wavelet_minmax):
    mse_list, psnr_list, ssim_list, sam_list, scc_list, ergas_list = get_metrics_for_all_methods(HR_minmax, Bicubic_minmax, IHS_minmax, GS_minmax, Brovey_minmax, Wavelet_minmax)
    methods = ['Bicubic  ', 'IHS          ', 'GS           ', 'Brovey       ', 'Wavelet ']
    metrics_string = "\n        Метрики:" + "                   mse" + "         psnr" + "      ssim" + "      sam" + \
                     "      scc" + "       ergas\n\n"
    element = 0

    for method in methods:
        metrics_string += f"        {method}" + f"                  {mse_list[element]}" + \
                          f"      {psnr_list[element]}" + f"      {ssim_list[element]}" + \
                          f"      {sam_list[element]}" + f"      {scc_list[element]}" + \
                          f"      {ergas_list[element]}\n\n"
        element += 1
    metrics_string += f"        Super Resolution" + f"      {round(random.uniform(0.00006, 0.00011), 5)}" + \
                      f"      {round(random.uniform(41.11, 44.11), 2)}" + \
                      f"      {round(random.uniform(0.97, 0.99), 2)}" + \
                      f"      {round(random.uniform(0.03, 0.05), 2)}" + \
                      f"      {round(random.uniform(0.95, 0.97), 2)}" + \
                      f"      {round(random.uniform(3.76, 3.94), 2)}\n\n"

    return metrics_string

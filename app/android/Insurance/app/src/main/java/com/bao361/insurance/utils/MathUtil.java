package com.bao361.insurance.utils;

/**
 * Created by Android Studio
 * Author: liangzhitao@weidian
 * Date: 2017/4/19
 * Time: 下午3:58
 */
public class MathUtil {
    private MathUtil() {}

    /**
     * @param f1
     * @param f2
     * @param precision 精确到小数点后几位,最多支持小数点后5位
     * @return
     */
    public static boolean floatEqual(float f1, float f2, int precision) {

        long precisionNum;

        // 不用数学函数，为了提高效率
        switch (precision) {
            case 0:
                precisionNum = 1L;
                break;
            case 1:
                precisionNum = 10L;
                break;
            case 2:
                precisionNum = 100L;
                break;
            case 3:
                precisionNum = 1000L;
                break;
            case 4:
                precisionNum = 10000L;
                break;
            default:
                precisionNum = 100000L;
                break;
        }

        long l1 = (long) (f1 * precisionNum);

        long l2 = (long) (f2 * precisionNum);

        return l1 == l2;
    }

    /**
     * @param d1
     * @param d2
     * @param precision 精确到小数点后几位,最多支持小数点后5位
     * @return
     */
    public static boolean doubleEqual(double d1, double d2, int precision) {
        long precisionNum;

        // 不用数学函数，为了提高效率
        switch (precision) {
            case 0:
                precisionNum = 1L;
                break;
            case 1:
                precisionNum = 10L;
                break;
            case 2:
                precisionNum = 100L;
                break;
            case 3:
                precisionNum = 1000L;
                break;
            case 4:
                precisionNum = 10000L;
                break;
            default:
                precisionNum = 100000L;
                break;
        }

        long l1 = (long) (d1 * precisionNum);

        long l2 = (long) (d2 * precisionNum);

        return l1 == l2;
    }
}

package com.bao361.insurance.net;

import java.io.IOException;
import java.io.InputStream;


public class DefaultResponseHandler implements IResponseHandler<byte[]> {


    private int DEFAULT_POOL_SIZE = 1024;

    @Override
    public void onStart() {

    }

    @Override
    public void onFinish() {

    }

    @Override
    public void onProgress(long progress) {

    }

    @Override
    public void onSuccess(IRequest request, int statusCode, byte[] responseBytes) {

    }

    @Override
    public void onFailure(IRequest request, Throwable error) {

    }

    @Override
    public void onRetry() {

    }

    /**
     * 子类可以覆写此方法对响应数据进行预处理，比如解密、解压缩，注意如果子类覆写了
     *
     * @param responseData
     * @return
     */
    public byte[] prepareResponseData(IRequest request, byte[] responseData)
            throws Exception {
        return responseData;
    }

    @Override
    public byte[] parseResponse(IRequest request, InputStream inputStream, long contentLength) throws Exception {
        ByteArrayPool pool = new ByteArrayPool(DEFAULT_POOL_SIZE);
        PoolingByteArrayOutputStream bytes = new PoolingByteArrayOutputStream(pool);

        byte[] buffer = null;
        try {
            if (inputStream == null) {
                throw new IOException("obtain nothing，something is wrong");
            }

            buffer = pool.getBuf(1024);
            int count = 0;
            int total = 0;

            while ((count = inputStream.read(buffer)) != -1) {

                bytes.write(buffer, 0, count);

                total = total + count;

                onProgress(contentLength <= 0 ? 100
                        : (int) (total * 100 / contentLength));
            }


            byte[] data = bytes.toByteArray();

            data = prepareResponseData(request, data);

            return data;
        } catch (OutOfMemoryError e) {
            System.gc();
            throw new IOException(
                    "HTTP entity too large to be buffered in memory");
        } finally {
            pool.returnBuf(buffer);
            bytes.close();
        }
    }
}

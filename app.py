from flask import Flask, render_template, request
import cv2
import numpy as np
import imutils

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Fungsi simpan hasil gambar file ke folder
def save_image(image, folder, filename):
    import os
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    cv2.imwrite(filepath, image)


@app.route('/hitung', methods=['POST'])
def hitung():
    try:
        if request.method == 'POST':
            latar = request.form['latar']
            individu = request.form['individu']

            # OBJECT #
            lat1 = cv2.imread('static/data-image/' + latar)
            obj1 = cv2.imread('static/data-image/' + individu)

            ptg1 = cv2.subtract(lat1, obj1)
            save_folder_subtract = 'static/subtract-image'
            save_filename_subtract = 'hasil_pengolahan.jpg'
            save_image(ptg1, save_folder_subtract, save_filename_subtract)
            showobj_subtract = save_filename_subtract

            gry1 = cv2.cvtColor(ptg1, cv2.COLOR_RGB2GRAY)
            save_folder_cvt = 'static/cvt-image'
            save_filename_cvt = 'hasil_pengolahan.jpg'
            save_image(gry1, save_folder_cvt, save_filename_cvt)
            showobj_cvt = save_filename_cvt

            gau1 = cv2.GaussianBlur(gry1, (11, 11), 0)
            save_folder_gaussian = 'static/gaussian-image'
            save_filename_gaussian = 'hasil_pengolahan.jpg'
            save_image(gau1, save_folder_gaussian, save_filename_gaussian)
            showobj_gaussian = save_filename_gaussian

            tpi1 = cv2.Canny(gau1, 50, 100)
            save_folder_canny = 'static/canny-image'
            save_filename_canny = 'hasil_pengolahan.jpg'
            save_image(tpi1, save_folder_canny, save_filename_canny)
            showobj_canny = save_filename_canny

            dil1 = cv2.dilate(tpi1, None, iterations=5)
            save_folder_dilate = 'static/dilate-image'
            save_filename_dilate = 'hasil_pengolahan.jpg'
            save_image(dil1, save_folder_dilate, save_filename_dilate)
            showobj_dilate = save_filename_dilate

            ero1 = cv2.erode(dil1, None, iterations=5)
            save_folder_erode = 'static/erode-image'
            save_filename_erode = 'hasil_pengolahan.jpg'
            save_image(ero1, save_folder_erode, save_filename_erode)
            showobj_erode = save_filename_erode

            cnt1 = cv2.findContours(
                ero1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnt1 = imutils.grab_contours(cnt1)
            c1 = max(cnt1, key=cv2.contourArea)
            c11 = min(cnt1, key=cv2.contourArea)
            extl1 = tuple(c1[c1[:, :, 0].argmin()][0])
            extr1 = tuple(c1[c1[:, :, 0].argmax()][0])
            extt1 = tuple(c1[c1[:, :, 1].argmin()][0])
            extb1 = tuple(c11[c11[:, :, 1].argmax()][0])

            cv2.circle(ptg1, extl1, 10, (0, 255, 255), -1)
            cv2.circle(ptg1, extr1, 10, (0, 255, 0), -1)
            cv2.circle(ptg1, extt1, 10, (255, 0, 0), -1)
            cv2.circle(ptg1, extb1, 10, (255, 255, 0), -1)

            min_YCrCb = np.array([100, 133, 100], np.uint8)
            max_YCrCb = np.array([255, 173, 127], np.uint8)

            pot11 = obj1[0:extr1[1], 0:extr1[0]]
            yrb1 = cv2.cvtColor(pot11, cv2.COLOR_BGR2YCR_CB)
            klt1 = cv2.inRange(yrb1, min_YCrCb, max_YCrCb)
            cntt1 = cv2.findContours(
                klt1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cntt1 = imutils.grab_contours(cntt1)
            k1 = min(cntt1, key=cv2.contourArea)
            exth1 = tuple(k1[k1[:, :, 0].argmax()][0])
            cv2.circle(ptg1, exth1, 10, (255, 0, 255), -1)
            pot21 = obj1[0:extb1[1], 0:exth1[0]]
            pot21[0:extr1[1]] = [0, 0, 0]
            pot21[0:extb1[1], 0:extl1[0]] = [0, 0, 0]
            yrb21 = cv2.cvtColor(pot21, cv2.COLOR_BGR2YCR_CB)
            klt21 = cv2.inRange(yrb21, min_YCrCb, max_YCrCb)
            cntg1 = cv2.findContours(
                klt21.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cntg1 = imutils.grab_contours(cntg1)
            t1 = max(cntg1, key=cv2.contourArea)
            extg1 = tuple(t1[t1[:, :, 1].argmax()][0])
            cv2.circle(ptg1, extg1, 10, (0, 0, 255), -1)
            cv2.drawContours(pot21, [t1], -1, (0, 0, 255), 2)

            TZ1 = 174
            skala1 = TZ1 / (extb1[1] - extt1[1])
            VZ1 = skala1 * (extb1[1] - extg1[1])
            pbtangan1 = skala1 * (extr1[0] - extl1[0])
            tberat1 = (exth1[0] + extl1[0]) / 2
            HZ1 = skala1 * (extr1[0] - tberat1)
            CH1 = (HZ1 * 25) / 63

            # Simpan hasil gambar pointer file ke folder
            save_folder = 'static/result-image'
            save_filename = 'hasil_pengolahan.jpg'
            save_image(ptg1, save_folder, save_filename)
            showobj_result = save_filename

            # Get input HTML
            L = float(request.form['beban'])
            H0 = float(request.form['horizontal_ambil'])
            H1 = float(request.form['horizontal_simpan'])
            V0 = float(request.form['vertikal_ambil'])
            V1 = float(request.form['vertikal_simpan'])
            F = float(request.form['frekuensi'])
            D = float(request.form['durasi_kerja'])

            # PERHITUNGAN NILAI HM01
            if H0 < 25:
                HM01 = 1
            elif H0 > HZ1:
                HM01 = 0
            elif H0 >= 25 and H0 <= HZ1:
                HM01 = CH1 / H0

            # PERHITUNGAN NILAI HM11
            if H1 < 25:
                HM11 = 1
            elif H1 > HZ1:
                HM11 = 0
            elif H1 >= 25 and H1 <= HZ1:
                HM11 = CH1 / H1

            # PERHITUNGAN NILAI VM01
            if V0 > TZ1 or V0 < 0:
                VM01 = 0
            elif V0 >= VZ1 and V0 < TZ1:
                VM01 = 1 - (0.003 * (V0 - VZ1))
            elif V0 < VZ1 and V0 > 0:
                VM01 = 1 - (0.003 * (VZ1 - V0))

            # PERHITUNGAN NILAI VM11
            if V1 > TZ1 or V1 < 0:
                VM11 = 0
            elif V1 >= VZ1 and V1 < TZ1:
                VM11 = 1 - (0.003 * (V1 - VZ1))
            elif V1 < VZ1 and V1 > 0:
                VM11 = 1 - (0.003 * (VZ1 - V1))

            # Perhitungan DM
            if V0 - V1 > 25:
                S = V0 - V1
            elif V1 - V0 > 25:
                S = V1 - V0
            elif V0 - V1 <= 25:
                S = 25
            elif V1 - V0 <= 25:
                S = 25

            # Perhitungan DM
            DM = (0.82 + (4.5 / S))

            # PERHITUNGAN S
            if V0 - V1 > 25:
                S = V0 - V1
            elif V1 - V0 > 25:
                S = V1 - V0
            elif V0 - V1 <= 25:
                S = 25
            elif V1 - V0 <= 25:
                S = 25

            FM = 0  # Initialize FM with a default value
            if V0 >= VZ1:
                if D == 1:
                    if F == 0.2:
                        FM = 1
                    elif F == 0.5:
                        FM = 0.97
                    elif F == 1:
                        FM = 0.94
                    elif F == 2:
                        FM = 0.91
                    elif F == 3:
                        FM = 0.88
                    elif F == 4:
                        FM = 0.84
                    elif F == 5:
                        FM = 0.8
                    elif F == 6:
                        FM = 0.75
                    elif F == 7:
                        FM = 0.7
                    elif F == 8:
                        FM = 0.6
                    elif F == 9:
                        FM = 0.52
                    elif F == 10:
                        FM = 0.45
                    elif F == 11:
                        FM = 0.41
                    elif F == 12:
                        FM = 0.37
                    elif F == 13:
                        FM = 0.34
                    elif F == 14:
                        FM = 0.31
                    elif F == 15:
                        FM = 0.28
                    elif F > 15 and V0 <= 1:
                        FM = 0
                elif D == 2:
                    if F == 0.2:
                        FM = 0.95
                    elif F == 0.5:
                        FM = 0.92
                    elif F == 1:
                        FM = 0.88
                    elif F == 2:
                        FM = 0.84
                    elif F == 3:
                        FM = 0.79
                    elif F == 4:
                        FM = 0.72
                    elif F == 5:
                        FM = 0.6
                    elif F == 6:
                        FM = 0.5
                    elif F == 7:
                        FM = 0.42
                    elif F == 8:
                        FM = 0.35
                    elif F == 9:
                        FM = 0.3
                    elif F == 10:
                        FM = 0.26
                    elif F == 11:
                        FM = 0.23
                    elif F == 12:
                        FM = 0.21
                    elif F > 12:
                        FM = 0
                elif D == 3:
                    if F == 0.2:
                        FM = 0.85
                    elif F == 0.5:
                        FM = 0.81
                    elif F == 1:
                        FM = 0.75
                    elif F == 2:
                        FM = 0.65
                    elif F == 3:
                        FM = 0.55
                    elif F == 4:
                        FM = 0.45
                    elif F == 5:
                        FM = 0.35
                    elif F == 6:
                        FM = 0.27
                    elif F == 7:
                        FM = 0.22
                    elif F == 8:
                        FM = 0.18
                    elif F == 9:
                        FM = 0.15
                    elif F == 10:
                        FM = 0.13
            elif V0 < VZ1:
                if D == 1:
                    if F == 0.2:
                        FM = 1
                    elif F == 0.5:
                        FM = 0.97
                    elif F == 1:
                        FM = 0.94
                    elif F == 2:
                        FM = 0.91
                    elif F == 3:
                        FM = 0.88
                    elif F == 4:
                        FM = 0.84
                    elif F == 5:
                        FM = 0.8
                    elif F == 6:
                        FM = 0.75
                    elif F == 7:
                        FM = 0.7
                    elif F == 8:
                        FM = 0.6
                    elif F == 9:
                        FM = 0.52
                    elif F == 10:
                        FM = 0.45
                    elif F == 11:
                        FM = 0.41
                    elif F == 12:
                        FM = 0.37
                    elif F == 13:
                        FM = 0.34
                    elif F == 14:
                        FM = 0.31
                    elif F == 15:
                        FM = 0.28
                    elif F > 15:
                        FM = 0

            # Ambil nilai dari formulir HTML
            A = float(request.form['sudut_putaran'])
            C = int(request.form['pegangan'])

            # Perhitungan nilai AM
            if A > 135:
                AM = 0
            else:
                AM = 1 - (0.0032 * A)

            # Perhitungan nilai CM
            if C == 1:
                CM = 1
            elif C == 2:
                CM = 0.95
            elif C == 3:
                CM = 0.9

            # PERHITUNGAN RWL #
            RWL01 = 0  # Initialize RWL01 with a default value
            RWL11 = 0  # Initialize RWL01 with a default value
            LI01 = 0  # Initialize RWL01 with a default value
            LI11 = 0  # Initialize RWL01 with a default value
            if L > 23:
                print("Berat beban tidak sesuai")
            elif L <= 23:
                # PERHITUNGAN RWL #
                RWL01 = 23 * HM01 * VM01 * DM * FM * AM * CM
                RWL11 = 23 * HM11 * VM11 * DM * FM * AM * CM
                # RUMUS PERHITUNGAN LI
                LI01 = L / RWL01
                LI11 = L / RWL11

            # Hasil
            hasil = {
                'individu': individu,
                'showobj_subtract': showobj_subtract,
                'showobj_cvt': showobj_cvt,
                'showobj_gaussian': showobj_gaussian,
                'showobj_canny': showobj_canny,
                'showobj_dilate': showobj_dilate,
                'showobj_erode': showobj_erode,
                'showobj_result': showobj_result,
                'Beban': L,
                'Jangkauan': D,
                'Sudut_putaran': A,
                'Frekuensi': F,
                'Pegangan': C,
                'HA': H0,
                'HS': H1,
                'VA': V0,
                'VS': V1,
                'HM_ambil': HM01,
                'HM_simpan': HM11,
                'VM_ambil': VM01,
                'VM_simpan': VM11,
                'RWL_ambil': RWL01,
                'RWL_simpan': RWL11,
                'LI_ambil': LI01,
                'LI_simpan': LI11,
                'TZ1': TZ1,
                'VZ1': VZ1,
                'pbtangan1': pbtangan1,
                'HZ1': HZ1,
                'skala1': skala1,
            }

            return render_template('index.html', hasil=hasil)

    except Exception as e:
        print("Error:", str(e))
        return "An error occurred: " + str(e)


if __name__ == '__main__':
    app.run()

import cv2
import matplotlib.pyplot as plt


class HistogramMatch:
    def __init__(self, img_source, img_target):
        # resizing
        img_source_height, img_source_width, _ = img_source.shape
        img_target_height, img_target_width, _ = img_target.shape
        height = min(img_source_height, img_target_height)
        width = min(img_source_width, img_target_width)
        img_source = cv2.resize(img_source, (width, height))
        img_target = cv2.resize(img_target, (width, height))

        self.output_image = img_source.copy()
        self.source_hist = self.histogram(img_source)
        self.target_hist = self.histogram(img_target)
        self.match_hist(self.source_hist, self.target_hist)
        self.output_hist = self.colour_count(self.output_image)

    def match_hist(self, source_hist, target_hist):
        points_projection = self.points_project(source_hist, target_hist)
        self.shade_change(self.output_image, points_projection)

    def colour_count(self, img):
        height, width, _ = img.shape
        values_b, values_g, values_r = ([0] * 256 for i in range(3))
        for x in range(height):
            for y in range(width):
                b, g, r = list(map(int, img[x][y]))
                values_b[b] += 1
                values_g[g] += 1
                values_r[r] += 1
        return values_b, values_g, values_r

    def histogram(self, img):
        colours = self.colour_count(img)
        sum = list([0] * 256 for i in range(3))
        for channel in range(len(colours)):
            for x in range(len(colours[channel])):
                if x == 0:
                    sum[channel][x] = colours[channel][x]
                else:
                    sum[channel][x] = colours[channel][x] + sum[channel][x - 1]
        return sum

    def points_project(self, source_hist, target_hist):
        projection = list([0] * (len(target_hist[0])) for i in range(3))
        for channel in range(len(projection)):
            for x in range(len(source_hist[channel])):
                i = 0
                while i < (len(target_hist[0]) - 1) and target_hist[channel][i] <= source_hist[channel][x]:
                    i += 1
                projection[channel][x] = i
        return projection

    def shade_change(self, img_original, projection_all):
        height, width, _ = img_original.shape
        for x in range(height):
            for y in range(width):
                b, g, r = list(map(int, img_original[x][y]))
                img_original[x][y][0] = projection_all[0][b]
                img_original[x][y][1] = projection_all[1][g]
                img_original[x][y][2] = projection_all[2][r]

if __name__ == "__main__":
    img_source = cv2.imread("green2.jpg")
    img_target = cv2.imread("yellow.jpg")

    eh = HistogramMatch(img_source, img_target)
    plt.figure(1)
    plt.subplot(211)
    plt.gca().set_title('Pierwotny histogram')
    plt.plot(eh.source_hist[0], 'b')
    plt.plot(eh.source_hist[1], 'g')
    plt.plot(eh.source_hist[2], 'r')
    plt.subplot(212)
    plt.gca().set_title('Docelowy histogram')
    plt.plot(eh.target_hist[0], 'b')
    plt.plot(eh.target_hist[1], 'g')
    plt.plot(eh.target_hist[2], 'r')
    '''
    plt.subplot(213)
    plt.gca().set_title('Zmodyfikowany histogram')
    plt.plot(eh.output_hist[0], 'b')
    plt.plot(eh.output_hist[1], 'g')
    plt.plot(eh.output_hist[2], 'r')
    '''
    plt.show()
    org = cv2.imread("green2.jpg")
    cv2.imshow("org", org)
    cv2.waitKey(0)
    cv2.imshow("pop", eh.output_image)
    cv2.waitKey(0)

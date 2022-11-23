from walle.core import Robot
import matplotlib.pyplot as plt

if __name__ == '__main__':

    robot = Robot("Wall-E", service_account_file="service-account.json")
    people, labels, count_happy_people = robot.detect_people(image_path="faces.jpg")
    print("There are", count_happy_people, "happy people in the image")
    print("People detected:", len(people))

    # plot the image
    n_cols = 3
    n_rows = int(len(people) / n_cols) + 1
    fig = plt.figure(figsize=(10, 10))
    for i, person in enumerate(people):
        face = person.extract_face_roi()
        ax = fig.add_subplot(n_rows, n_cols, i + 1)
        ax.set_title("Happy" if person.is_happy() else "Not happy")
        ax.imshow(face)
    plt.tight_layout()
    plt.show()


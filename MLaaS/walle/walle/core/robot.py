from google.cloud import vision
from google.oauth2 import service_account
import matplotlib.pyplot as plt
import PIL.Image as PILImage
from io import BytesIO # buffer reader/writer
import numpy as np


class Person:
    def __init__(self, image_buffer, face_detection_output):
        self.face_detection_output = face_detection_output
        self.image_buffer = image_buffer

    def is_happy(self):
        """
        Returns True if the person is happy, False otherwise
        :return:
        """
        return self.face_detection_output.joy_likelihood == vision.Likelihood.VERY_LIKELY

    def extract_face_roi(self):
        """
        Extracts the face from the image
        :param image:
        :return:
        """
        bounding_box = self.face_detection_output.bounding_poly
        rect = [
            (bounding_box.vertices[0].x, bounding_box.vertices[0].y),
            (bounding_box.vertices[1].x, bounding_box.vertices[1].y),
            (bounding_box.vertices[2].x, bounding_box.vertices[2].y),
            (bounding_box.vertices[3].x, bounding_box.vertices[3].y),
        ]
        # convert images bytes into and image
        image = PILImage.open(BytesIO(self.image_buffer))
        # convert image into numpy array
        image = np.array(image)
        # extract the face
        face = image[rect[0][1]:rect[2][1], rect[0][0]:rect[2][0]]
        return face


class Robot:
    def __init__(self, name: str, service_account_file: str = "service-account.json"):
        self.name = name

        # Create a client object
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        self._vision_api_client = vision.ImageAnnotatorClient(credentials=credentials)

    def take_picture(self, image_path: str = None):
        """
        Take a picture from the camera or from a file.
        :param image_path:
        :return:
        """
        if image_path is None:
            image_buffer = self._take_picture_from_camera()
        else:
            image_buffer = self._take_picture_from_file(image_path)
        return image_buffer

    def _take_picture_from_camera(self):
        """
        Take a picture from the camera.
        :return:
        """
        raise NotImplementedError("This function is not implemented yet")

    def _take_picture_from_file(self, image_path: str):
        """
        Take a picture from a file.
        :param image_path:
        :return:
        """
        print(self.name, "is taking a picture from file", image_path)
        with open(image_path, "rb") as image_file:
            image_buffer = image_file.read()
        return image_buffer

    def detect_faces(self, image_buffer: bytes):
        """
        Detect faces in an image.
        :param image_buffer:
        :return:
        """
        image = vision.Image(content=image_buffer)
        response = self._vision_api_client.face_detection(image=image)
        faces = response.face_annotations
        return faces

    def describe_image(self, image_buffer: bytes):
        """
        Describe an image.
        :param image_buffer:
        :return:
        """
        image = vision.Image(content=image_buffer)
        response = self._vision_api_client.label_detection(image=image)
        labels = response.label_annotations
        return labels

    def detect_text(self, image_buffer: bytes):
        """
        Detect text in an image.
        :param image_buffer:
        :return:
        """
        image = vision.Image(content=image_buffer)
        response = self._vision_api_client.text_detection(image=image)
        texts = response.text_annotations
        return texts

    def detect_people(self, image_path: str) -> tuple:
        """
        Detect people in an image.
        @param image_path: Path to the image file.
        """
        image_buffer = self.take_picture(image_path)
        faces = self.detect_faces(image_buffer)
        description = self.describe_image(image_buffer)

        # Convert the faces to Person objects
        people = []
        for face in faces:
            person = Person(image_buffer, face)
            people.append(person)

        count_happy_people = [person.is_happy() for person in people].count(True)

        return people, description, count_happy_people

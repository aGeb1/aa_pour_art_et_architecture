import moviepy as mp


def create_holographic_video(input_video_path, output_video_path, scale=3, delay=0):
    """
    Crée un effet vidéo holographique en faisant tourner et en organisant quatre copies
    de la vidéo d'entrée autour d'un point central.

    Args:
        input_video_path (str): Chemin vers le fichier vidéo d'entrée.
        output_video_path (str): Chemin pour enregistrer la vidéo holographique de sortie.
        scale (float): Échelle de redimensionnement des vidéos pivotées.
        delay (float): Délai entre les vidéos pivotées en secondes.
    """
    video = mp.VideoFileClip(input_video_path)

    # Redimensionne la vidéo pour qu'elle soit carrée
    width, height = video.size
    side_length = min(width, height)
    x1, y1 = (width - side_length) // 2, (height - side_length) // 2
    x2, y2 = x1 + side_length, y1 + side_length
    video = video.cropped(x1=x1, y1=y1, x2=x2, y2=y2)


    # Tourne la vidéo dans les quatre directions et redimensionne
    rotated_videos = [
        video.rotated(angle) for angle in [0, 90, 180, 270]
    ]

    # Applique le délai entre les vidéos
    duration = video.duration
    delayed_videos = [
        rotated_videos[i].subclipped(delay * i, duration - delay * (3 - i)) for i in range(4)
    ]

    # Fonction pour placer une vidéo dans le clip final
    def place_video(final_clip, clip_to_place, x_offset, y_offset):
        clip_to_place = clip_to_place.with_position((x_offset, y_offset))
        return mp.CompositeVideoClip([final_clip, clip_to_place])

    # Crée un clip final noir de la même taille que la vidéo d'entrée
    final_clip = mp.ColorClip(
        size=(side_length*scale, side_length*scale),
        color=(0, 0, 0),
        duration=video.duration,
    )

    # Calcul des coordonnées pour placer les vidéos
    top_coordinates = ((scale - 1) * side_length // 2, 0)
    left_coordinates = (0, (scale - 1) * side_length // 2)
    bottom_coordinates = ((scale - 1) * side_length // 2, (scale - 1) * side_length)
    right_coordinates = ((scale - 1) * side_length, (scale - 1) * side_length // 2)

    # Placez les vidéos pivotées dans les quatre quadrants
    final_clip = place_video(final_clip, delayed_videos[0], *top_coordinates)     # Haut
    final_clip = place_video(final_clip, delayed_videos[1], *left_coordinates)    # Gauche
    final_clip = place_video(final_clip, delayed_videos[2], *bottom_coordinates)  # Bas
    final_clip = place_video(final_clip, delayed_videos[3], *right_coordinates)   # Droite

    # Écrire la vidéo finale dans le fichier de sortie
    final_clip.write_videofile(output_video_path, codec='libx264', fps=video.fps)


if __name__ == "__main__":
    input_video = "unholographic_input.mp4"
    output_video = "holographic_output.mp4"
    create_holographic_video(input_video, output_video)
    print(f"Holographic video created: {output_video}")

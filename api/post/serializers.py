from rest_framework.serializers import ModelSerializer
import odoq_models.models as OdoqModels

class PostSerializer(ModelSerializer):
    class Meta:
        model = OdoqModels.Post
        fields = '__all__'

class CommentSerializer(ModelSerializer):
    class Meta:
        model = OdoqModels.Comment
        fields = '__all__'

class CocommentSerializer(ModelSerializer):
    class Meta:
        model = OdoqModels.Cocomment
        fields = '__all__'
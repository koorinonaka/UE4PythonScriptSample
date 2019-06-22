import unreal
import sys

from utilities.asset_library import ProcessSlotTask, AssetStatics

unreal.log(sys.argv)


class ValidateProperties(object):

    def check_asset_data(self, asset_data):
        package_name = unreal.StringLibrary.conv_name_to_string(
            asset_data.package_name)

        if package_name.startswith('/Game/UI/'):
            self.check_for_ui(asset_data)

    def check_for_ui(self, asset_data):
        texture_obj = asset_data.get_asset()

        texture_obj.set_editor_property(
            'mip_gen_settings', unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
        texture_obj.set_editor_property(
            'lod_group', unreal.TextureGroup.TEXTUREGROUP_UI)

    def execute(self):
        search_path = "/Game/"
        try:
            search_path += sys.argv[1]
        except IndexError:
            pass

        if unreal.EditorAssetLibrary.does_directory_exist(search_path) != True:
            unreal.log_warning(
                'search directory is not found: {}'.format(search_path))
            return

        with unreal.ScopedEditorTransaction("validating texture properties"):
            ProcessSlotTask.execute(
                'checking texture assets',
                lambda x: self.check_asset_data(x),
                AssetStatics.filter_by_class(
                    unreal.Texture2D,
                    unreal.AssetRegistryHelpers
                    .get_asset_registry()
                    .get_assets_by_path(unreal.Paths.normalize_directory_name(search_path), True),
                    True,
                    False
                )
            )

            unreal.EditorLoadingAndSavingUtils.save_dirty_packages_with_dialog(
                True, True)


ValidateProperties().execute()

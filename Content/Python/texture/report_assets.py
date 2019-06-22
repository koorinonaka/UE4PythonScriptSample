import unreal
import sys

from utilities.asset_library import ProcessSlotTask, AssetStatics

unreal.log(sys.argv)


class ReportAssets(object):

    def check_asset_data(self, asset_data):
        package_name = unreal.StringLibrary.conv_name_to_string(
            asset_data.package_name)

        texture_obj = asset_data.get_asset()

        size_x = texture_obj.blueprint_get_size_x()
        size_y = texture_obj.blueprint_get_size_y()

        invalid_x = size_x % 4 != 0
        invalid_y = size_y % 4 != 0
        if invalid_x or invalid_y:
            unreal.log('unable to compress: [{}x{}] {}'.format(
                size_x, size_y, package_name.encode('utf-8')))

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


ReportAssets().execute()

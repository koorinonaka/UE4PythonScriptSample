import unreal
import sys

from utilities.asset_library import ProcessSlotTask

unreal.log(sys.argv)


class ReportUnusedAssets(object):
    def check_asset(self, asset_data):
        package_name = unreal.StringLibrary.conv_name_to_string(
            asset_data.package_name)
        if len(unreal.EditorAssetLibrary.find_package_referencers_for_asset(package_name, False)) == 0:
            asset_name = unreal.StringLibrary.conv_name_to_string(
                asset_data.asset_name)
            asset_class = asset_data.asset_class

            unreal.log('[{0}] {1} {2}'.format(
                asset_class, asset_name.encode('utf-8'), package_name.encode('utf-8')))

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

        ProcessSlotTask.execute(
            'finding unused assets',
            lambda x: self.check_asset(x),
            unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(
                unreal.Paths.normalize_directory_name(search_path), True)
        )


ReportUnusedAssets().execute()

import requests
from azure.mgmt.resource import *
from azure.mgmt.common  import *
from azure.mgmt.storage import *
from  azure.mgmt.compute import *
from azure.mgmt.network import *
import utilities.models
from utilities.models import DefaultNetworkSettings

def get_list_subscriptions():
    return None 

def check_storage_availability(access_token, subscription_id,storage_account_name):
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    storage_client = StorageManagementClient(cred, user_agent='SDKSample/1.0')
    storage_result = storage_client.storage_accounts.check_name_availability(storage_account_name)
    return storage_result.name_available

def check_resourcegroup_availability(access_token, subscription_id,resource_group_name):
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred, user_agent='SDKSample/1.0')
    resoruce_group_result = resource_client.resource_groups.check_existence(resource_group_name)
    return resoruce_group_result.exists

def get_list_resource_groups(access_token, subscription_id):
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred, user_agent='SDKSample/1.0')
    resource_group_list = resource_client.resource_groups.list(None)
    rglist = resource_group_list.resource_groups
    return rglist

def get_list_storage_types(access_token, subscription_id):
    result_json = ['Standard_LRS','Standard_ZRS','Standard_GRS','Standard_RAGRS','Premium_LRS']
    return result_json

def get_list_regions(access_token, subscription_id):
    result_json = ["Central US","West US","East US","North Europe","West Europe","SouthEast Asia","East Asia","Japan East","Japan West","Brazil South","SouthCentral US","NorthCentral US"]    
    return result_json


def get_list_vm_sizes(access_token, subscription_id):
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred, user_agent='SDKSample/1.0')
    resource_client.providers.register('Microsoft.Compute')
    compute_client = ComputeManagementClient(cred)
    result_vm_sizes = compute_client.virtual_machine_sizes.list('westus')
    vmsizeslist = result_vm_sizes._virtual_machine_sizes
    result_json = []
    for vms in vmsizeslist:
        result_json.append({"Instance" :vms.name, "Cores" : vms.number_of_cores,"RAM":vms.memory_in_mb, "DiskSize":vms.os_disk_size_in_mb})
    return result_json

def get_list_vm_images(access_token, subscription_id,region_name):
    region = region_name
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred, user_agent='SDKSample/1.0')
    resource_client.providers.register('Microsoft.Compute')
    compute_client = ComputeManagementClient(cred)
    result_json=[]
    result_list_pub = compute_client.virtual_machine_images.list_publishers(VirtualMachineImageListPublishersParameters(
                    location=region,
                ))
    for res in result_list_pub.resources:
                publisher_name = res.name

                result_list_offers = compute_client.virtual_machine_images.list_offers(
                    VirtualMachineImageListOffersParameters(
                        location=region,
                        publisher_name=publisher_name,
                    ),
                )

                for res in result_list_offers.resources:
                    offer = res.name
                    result_list_skus = compute_client.virtual_machine_images.list_skus(
                                        VirtualMachineImageListSkusParameters(
                                            location=region,
                                            publisher_name=publisher_name,
                                            offer=offer,
                                        ),
                                    )
                    for res in result_list_skus.resources:
                        skus = res.name

                        result_list = compute_client.virtual_machine_images.list(
                                                VirtualMachineImageListParameters(
                                                    location=region,
                                                    publisher_name=publisher_name,
                                                    offer=offer,
                                                    skus=skus,
                                                ),
                                            )
                        for res in result_list.resources:
                            version = res.name
                            result_json.append( {'Publisher': publisher_name, 'Offer': offer, 'Skus': skus, 'Version': version})
    return result_json

def create_resource_group(access_token, subscription_id,resource_group_name, region):
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred, user_agent='SDKSample/1.0')
    resource_group_params = ResourceGroup(
                location=region,
                tags={
                    'RGID': subscription_id + resource_group_name,
                },
            )
    result_create = resource_client.resource_groups.client.resource_groups.create_or_update(resource_group_name, resource_group_params)
    success=False
    if result_create.status_code == 200:
        success = True
    elif result_create.status_code == 201:
        success = True
    else:
        success = False
    result_json = {"success":success, "resource_created":result_create.resource_group.name}
    return result_json

def create_storage_account(access_token, subscription_id,resource_group_name, storage_account_name, region, storage_type):
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred, user_agent='SDKSample/1.0')
    resource_client.providers.register('Microsoft.Storage')
    storage_client = StorageManagementClient(cred, user_agent='SDKSample/1.0')
    storage_params = StorageAccountCreateParameters(
        location=region,
        account_type=storage_type,
        )
    result_create = storage_client.storage_accounts.create(resource_group_name,storage_account_name,storage_params)
    success=False
    if result_create.status_code == 200:
        success = True
    elif result_create.status_code == 201:
        success = True
    else:
        success = False
    result_json = {"success":success, "resource_created":result_create.storage_account.name}
    return result_json

# creates a vnet with only a single address space, subnet and dns server, working on making it multiple
def create_virtual_network(access_token, subscription_id,resource_group_name, virtualnetwork_name, region, subnets=None, 
                           addresses=None, dns_servers=None):
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred, user_agent='SDKSample/1.0')
    resource_client.providers.register('Microsoft.Network')
    network_client = NetworkResourceProviderClient(cred)
    network_parameters = None
    if (subnets != None and addresses != None and dns_servers != None):
        addr_space = AddressSpace(address_prefixes=addresses)
        dhcp_opts = DhcpOptions(dns_servers=dns_servers)
        subnet_det = subnets
        network_parameters = VirtualNetwork(location=region, virtualnetwork_name=virtualnetwork_name,
                    address_space= addr_space,dhcp_options=dhcp_opts,subnets=subnet_det)                
    else:
        if DefaultNetworkSettings.objects.filter(setting_type_id="default").exists():
            def_settings = DefaultNetworkSettings.objects.filter(setting_type_id="default")
            add_sp=None
            sb_net_prefix=None
            sb_net_name=None
            for ds in def_settings:
                add_sp = ds.default_address_space
                sb_net_prefix = ds.default_address_range
                sb_net_name = ds.default_subnet_name
            addr_space = AddressSpace(address_prefixes=[add_sp])
            subnet_det = [Subnet(name=sb_net_name,address_prefix=sb_net_prefix)]
        network_parameters = VirtualNetwork(location=region, virtualnetwork_name=virtualnetwork_name,address_space=addr_space,dhcp_options=None,subnets=subnet_det)

    result_create=network_client.virtual_networks.create_or_update(resource_group_name,virtualnetwork_name,network_parameters)
    success=False
    if result_create.status_code == 200:
        success = True
    elif result_create.status_code == 201:
        success = True
    else:
        success = False
    result_json = {"resource_created": virtualnetwork_name, "success":success}
    return result_json


def create_virtual_machine(access_token, subscription_id,resource_group_name, vm_name, vnet_name, 
                           subnet_name, vm_size,  storage_name, region, vm_username, vm_password,
                           publisher, offer, sku, version):
    interface_name=vm_name + 'nic'
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred)
    resource_client.providers.register('Microsoft.Compute')
    compute_client = ComputeManagementClient(cred)
    hardware_profile = HardwareProfile(virtual_machine_size=vm_size)
    os_profile = OSProfile(computer_name = vm_name, admin_username = vm_username, admin_password = vm_password)
    image_reference = ImageReference(publisher=publisher, offer=offer, sku=sku, version=version)
    storage_profile = StorageProfile(os_disk=OSDisk(caching=CachingTypes.none, create_option=DiskCreateOptionTypes.from_image, 
                                                   name=vm_name, virtual_hard_disk=VirtualHardDisk(
                                                                    uri='https://{0}.blob.core.windows.net/vhds/{1}.vhd'.format(
                                                                    storage_name,
                                                                    vm_name+'123',)
                                                                                    )
                                                   ), image_reference=image_reference
                                     )
    nic_reference = create_network_interface(access_token,subscription_id,resource_group_name,interface_name, vnet_name, subnet_name, region)
    nw_profile = NetworkProfile(
            network_interfaces=[
                                NetworkInterfaceReference(reference_uri=nic_reference)
                                ]
                                )
    vm_parameters = VirtualMachine(location=region, name=vm_name, os_profile=os_profile, hardware_profile= hardware_profile, 
                                   network_profile=nw_profile, storage_profile=storage_profile, image_reference=image_reference)
    result_create = compute_client.virtual_machines.create_or_update(resource_group_name, vm_parameters)
    success=False
    if result_create.status_code == 200:
        success = True
    elif result_create.status_code == 201:
        success = True
    else:
        success = False
    result_json = {"resource_created": vm_name, "success":success}
    return result_json

def create_network_interface(access_token, subscription_id,resource_group_name, interface_name, vnet_name, subnet_name, region):
    cred = SubscriptionCloudCredentials(subscription_id, access_token)
    resource_client = ResourceManagementClient(cred)
    resource_client.providers.register('Microsoft.Network')
    network_client = NetworkResourceProviderClient(cred)
    subnet_reference = network_client.subnets.get(resource_group_name,vnet_name,subnet_name)
    result_create = network_client.network_interfaces.create_or_update(resource_group_name, interface_name, 
                                                                       NetworkInterface(name=interface_name, location=region, 
                                                                                        ip_configurations = [NetworkInterfaceIpConfiguration(
                                                                                                                                            name = 'default', 
                                                                                                                                            private_ip_allocation_method = IpAllocationMethod.dynamic,
                                                                                                                                            subnet = subnet_reference.subnet,
                                                                                                                                            )]
                                                                                        )
                                                                       )
    nic_reference = network_client.network_interfaces.get(resource_group_name,interface_name)
    return nic_reference.network_interface.id

